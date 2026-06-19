#include <ctime>
#include <fstream>
#include <iostream>
#include "raspicam/raspicam.h"
#include "raspicam/raspicam_cv.h"
#include <unistd.h>
#include <chrono>
#include <ctime>
#include <opencv2/opencv.hpp>
#include <wiringPi.h>

using namespace std;
using namespace cv;
using namespace raspicam;

//Camera Variables
Mat frame, Matrix, framePers, frameGray, frameThresh, frameEdge, frameFinal; 	// Variables to initialize each frame captures by camera
Mat ROILane, frameFinalDuplicate;
int LeftLanePos, RightLanePos, frameCenter, laneCenter, Result;
RaspiCam_Cv Camera;		// Global Camera Object
stringstream ss;		// Display string on stream
vector<int> histogramLane;

//Machine Learning Variables
CascadeClassifier Stop_Cascade;
Mat frame_Stop, ROI_Stop, gray_Stop;
vector<Rect> Stop;
int dist_stop;

//Setting POV Dimensions
Point2f Source[] = {Point2f(50,160),Point2f(350,160),Point2f(0,230), Point2f(400,230)};		// Camera view with drawn later with red lines
Point2f Destination[] = {Point2f(60,0),Point2f(340,0),Point2f(60,240), Point2f(340,240)};	// Birds eye perspective


/*       |(0,0)      			|
 *       |      			|
 *       |      			|
 *       |L      			|   Width  0 - 400 = x
 *       |      			|   Length 0 - 240 = y
 *       |      			|   
 *       |         W			|(400,240)   
 */

/*
 * Camera settings
 * 
 */
void Setup ( int argc,char **argv, RaspiCam_Cv &Camera )
{
    Camera.set ( CAP_PROP_FRAME_WIDTH,  ( "-w",argc,argv,400 ) );
    Camera.set ( CAP_PROP_FRAME_HEIGHT,  ( "-h",argc,argv,240 ) );
    Camera.set ( CAP_PROP_BRIGHTNESS, ( "-br",argc,argv,60 ) );
    Camera.set ( CAP_PROP_CONTRAST ,( "-co",argc,argv,50 ) );
    Camera.set ( CAP_PROP_SATURATION,  ( "-sa",argc,argv,55 ) );
    Camera.set ( CAP_PROP_GAIN,  ( "-g",argc,argv ,50 ) );
    Camera.set ( CAP_PROP_FPS,  ( "-fps",argc,argv,100));
}



/*
 * This Function I created shows the lines in color
 * Commented out green but that is the birds eye perspective
 * 
 */
void Perspective()
{
	line(frame,Source[0], Source[1], Scalar(0,0,255), 2);
	line(frame,Source[1], Source[3], Scalar(0,0,255), 2);
	line(frame,Source[3], Source[2], Scalar(0,0,255), 2);
	line(frame,Source[2], Source[0], Scalar(0,0,255), 2);
	
	//line(frame,Destination[0], Destination[1], Scalar(0,255,0), 2);
	//line(frame,Destination[1], Destination[3], Scalar(0,255,0), 2);
	//line(frame,Destination[3], Destination[2], Scalar(0,255,0), 2);
	//line(frame,Destination[2], Destination[0], Scalar(0,255,0), 2);
	
	Matrix = getPerspectiveTransform(Source, Destination);
	warpPerspective(frame, framePers, Matrix, Size(400,240));
}

/*
 * Calls the camera function. Captures what the camera is 
 * seeing. Putting this inside a while loop creates a video
 * 
 */
void Capture()
{
	Camera.grab();
	Camera.retrieve(frame);
	Camera.retrieve(frame_Stop);
}

/*
 * Using the live video stream, use threshold to change
 * the color values to eliminate all noise except lane. 
 * 
 */
void Threshold()
{
	cvtColor(framePers, frameGray, COLOR_RGB2GRAY);
	inRange(frameGray, 128, 255, frameThresh);
	Canny(frameGray,frameEdge, 600, 900, 3, false);
	add(frameThresh, frameEdge, frameFinal);
	cvtColor(frameFinal, frameFinal, COLOR_GRAY2RGB);
	cvtColor(frameFinal, frameFinalDuplicate, COLOR_RGB2BGR); //for histogram
}

/*
 * Need to generate a histogram and also splitting the 
 * perspective into multiple vectors to identify lane shift
 * 
 */
void Histogram()
{
	histogramLane.resize(400);
	histogramLane.clear();
	
	for(int i=0; i<400; i++) //frame.size().width = 400
	{
		ROILane = frameFinalDuplicate(Rect(i,140,1,100)); //here
		divide(255, ROILane, ROILane);
		histogramLane.push_back((int)(sum(ROILane)[0]));
	}
}


/*
 * Returns actual position of left lane with respect to left border 
 * Returns actual position of right lane with respect to right border 
 */
void LaneFinder()
{
	vector<int>:: iterator LeftPtr;
	LeftPtr = max_element(histogramLane.begin(), histogramLane.begin() + 150); //had to use 150 instead of 200 because of +-50 error in processing time	
	LeftLanePos = distance(histogramLane.begin(), LeftPtr); 

	vector<int>:: iterator RightPtr;
	RightPtr = max_element(histogramLane.begin() +250, histogramLane.end()); //had to use 150 instead of 200 because of +-50 error in processing time	
	RightLanePos = distance(histogramLane.begin(), RightPtr); 
	
	line(frameFinal, Point2f(LeftLanePos,0), Point2f(LeftLanePos,240), Scalar(0,255,0),2);
	line(frameFinal, Point2f(RightLanePos,0), Point2f(RightLanePos,240), Scalar(0,255,0),2);
}


void LaneCenter()
{
	laneCenter = (RightLanePos-LeftLanePos)/2 + LeftLanePos;
	frameCenter = 195;
	line(frameFinal, Point2f(laneCenter,0), Point2f(laneCenter,240), Scalar(0,255,0),3);
	line(frameFinal, Point2f(frameCenter,0), Point2f(frameCenter,240), Scalar(255,0,0),3);
	Result = laneCenter-frameCenter;

}

void Stop_detection()
{
    if(!Stop_Cascade.load("//home//platinum//project//MachineLearning//cascade.xml"))
    {
	printf("Failed to load ML Cascade file");
    }
    
    ROI_Stop = frame_Stop(Rect(0,0,200,240));
    //cvtColor(ROI_Stop, gray_Stop, COLOR_RGB2GRAY);
    //cvtColor(ROI_Stop, gray_Stop, COLOR_RGB2BGR);
    // equalizeHist(gray_Stop, gray_Stop);
    Stop_Cascade.detectMultiScale(ROI_Stop, Stop);
    for(int i=0; i<Stop.size(); i++)
    {
		Point P1(Stop[i].x, Stop[i].y);
		Point P2(Stop[i].x + Stop[i].width, Stop[i].x + Stop[i].height);
		rectangle(ROI_Stop, P1, P2, Scalar(0,0,255), 2); // creates rectangle around stop sign
        dist_stop = (-2)*(P2.x-P1.x)+140; //b adjusted 
        
        ss.str(" ");
		ss.clear();
		//ss<<"Dist = "<<P2.x-P1.x<<"pix";
		ss<<"Dist = "<<dist_stop<<"cm";
		putText(frame, ss.str(), Point2f(1,30), 0,1, Scalar(0,0,255), 2);
		
		//Car from stop sign = 17.5 inches(45cm) 50px
		//Car from stop sign = 10   inches(25cm) 56px
		//y=mx+b   44.45 = 50m + b
		//		   25.40 = 56m + b
		//m = -2 b = 145	
    }
    
}

int main(int argc,char **argv)
{
    wiringPiSetup();
    pinMode(21, OUTPUT);
    pinMode(22, OUTPUT);
    pinMode(23, OUTPUT);
    pinMode(24, OUTPUT);
	
	
    Setup(argc, argv, Camera);
    cout<<"Connecting to camera"<<endl;
    if (!Camera.open())
    {
	cout<<"Failed to Connect"<<endl;
    }
     
    cout<<"Camera Id = "<<Camera.getId()<<endl;
     
     
     
    while(1)
    {
	auto start = std::chrono::system_clock::now(); 	//get time when the camera opens
		
	Capture();
	Perspective();
	Threshold();
	Histogram();
	LaneFinder();
	LaneCenter();
	Stop_detection();
	
	if(dist_stop > 5 && dist_stop < 20)
	{
		digitalWrite(21, 1);
		digitalWrite(22, 1);
		digitalWrite(23, 1);
		digitalWrite(24, 0);
		
		cout<<"STOP"<<endl;
		dist_stop = 0;
		goto Stop_Sign;
	}
		
//Binary digital write
//FORWARD
	if(Result == 0)
	{
		digitalWrite(21, 0);
		digitalWrite(22, 0);
		digitalWrite(23, 0);
		digitalWrite(24, 0);
		
		cout<<"FORWARD"<<endl;
	}
	else if(Result > 0 && Result < 10) //RIGHT
	{	//Decimal 1
		digitalWrite(21, 1);
		digitalWrite(22, 0);
		digitalWrite(23, 0);
		digitalWrite(24, 0);
		
		cout<<"RIGHT1"<<endl;
	}
	else if(Result >= 10 && Result <= 20)
	{	//Decimal 2 Works
		digitalWrite(21, 0);
		digitalWrite(22, 1);
		digitalWrite(23, 0);
		digitalWrite(24, 0);
		
		cout<<"RIGHT2"<<endl;
	}
	else if(Result > 20)
	{	//Decimal 3
		digitalWrite(21, 1);
		digitalWrite(22, 1);
		digitalWrite(23, 0);
		digitalWrite(24, 0);
		
		cout<<"RIGHT3"<<endl;
	}
	else if(Result < 0 && Result > -10)//LEFT
	{	//Decimal 4 works
		digitalWrite(21, 0);
		digitalWrite(22, 0);
		digitalWrite(23, 1);
		digitalWrite(24, 0);
		
		cout<<"LEFT1"<<endl;
	}
	else if(Result <= -10 && Result >= -20)
	{	//Decimal 5
		digitalWrite(21, 1);
		digitalWrite(22, 0);
		digitalWrite(23, 1);
		digitalWrite(24, 0);
		
		cout<<"LEFT2"<<endl;
	}
	else if(Result < -20)
	{ 	//Decimal 6 works
		digitalWrite(21, 0);
		digitalWrite(22, 1);
		digitalWrite(23, 1);
		digitalWrite(24, 0);
		
		cout<<"LEFT3"<<endl;
	}
	Stop_Sign:
	
		ss.str(" ");
		ss.clear();
		ss<<"Result = "<<Result;
		putText(frame, ss.str(), Point2f(1,50), 0,1, Scalar(0,0,255), 2);

		namedWindow("Original", WINDOW_KEEPRATIO);
		//moveWindow("Original", 0, 100);
		//resizeWindow("Original", 640, 480);
		imshow("Original", frame);
			
		//namedWindow("Perspective", WINDOW_KEEPRATIO);
		//moveWindow("Perspective", 640, 100);
		//resizeWindow("Perspective", 640, 480);
		//imshow("Perspective", framePers);

		namedWindow("GrayScale", WINDOW_KEEPRATIO);
		//moveWindow("GrayScale", 1280, 100);
		//resizeWindow("GrayScale", 640, 480);
		imshow("GrayScale", frameGray);
		
		//namedWindow("GrayScale", WINDOW_KEEPRATIO);
		//moveWindow("GrayScale", 1280, 100);
		//resizeWindow("GrayScale", 640, 480);
		//imshow("GrayScale", frameEdge);

		namedWindow("Final", WINDOW_KEEPRATIO);
		//moveWindow("Final", 1280, 100);
		//resizeWindow("Final", 640, 480);
		imshow("Final", frameFinal);
		
		namedWindow("Stop Sign", WINDOW_KEEPRATIO);
		//moveWindow("Final", 1280, 100);
		//resizeWindow("Final", 640, 480);
		imshow("Stop Sign", ROI_Stop);
		
		waitKey(1);
		
		auto end = std::chrono::system_clock::now();  	//get time when camera retrieves frame
	  
		std::chrono::duration<double> elapsed_seconds = end-start;
		
		float t = elapsed_seconds.count();
		int FPS = 1/t;  								//calculating frames per second
		cout<<"FPS = "<<FPS<<endl;
	  
    }

    return 0;   
}
