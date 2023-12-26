function varargout = Project2GUI(varargin)
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @Project2GUI_OpeningFcn, ...
                   'gui_OutputFcn',  @Project2GUI_OutputFcn, ...
                   'gui_LayoutFcn',  [], ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
   gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end

% --- Executes just before Project2GUI is made visible.
function Project2GUI_OpeningFcn(hObject, eventdata, handles, varargin)
handles.output = hObject;
guidata(hObject, handles);

function varargout = Project2GUI_OutputFcn(hObject, eventdata, handles)
varargout{1} = handles.output;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% LOAD FUNCTION %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function loadvideo_Callback(hObject, eventdata, handles) %#ok<*DEFNU>
[filename,filepath] = uigetfile('*.*','Please select a file');
if ~filename % if error 
  return
end;
videoinfo = strcat(filepath, filename);
set(gcf,'Color',[0 0 0]); % after loading the file, background changed to black(cinema mode)
videoinfo = VideoReader(videoinfo);% Obtain the video file, and get it's information

% Obtain info from handles
movName = videoinfo.Name;            
movHeight = videoinfo.Height;        
movWidth = videoinfo.Width;          
movFrameRate = videoinfo.FrameRate;
movTime = videoinfo.duration; 
hours=movTime/3600;
hours=floor(hours);
movTime=movTime-hours*3600;
minutes=movTime/60;
minutes=floor(minutes);
movTime=movTime-minutes*60;
seconds=movTime;
handles.NumberOfFrame=videoinfo.NumberOfFrame; % total frame of the video
handles.videoinfo=videoinfo; % store mov info to handles.videoinfo
handles.CurrentFrame=1; % initialize the current frame 

%Displays the following features on the GUI
movName1 = sprintf('File Name: %s \n',movName);
movResolution1 = sprintf('Resolution: %g x %g \n',movWidth,movHeight);
movFrameRate1 = sprintf('Frame Rate: %g \n',movFrameRate);
movTime1 = sprintf('Total Duration: %0.f hr %.f min %.f s \n',hours,minutes,seconds);

%Make it into structure so it displays the information ontop of each other 
infomov(1,1)={movName1}; 
infomov(2,1)={movResolution1};
infomov(3,1)={movFrameRate1};
infomov(4,1)={movTime1};

% slider
set(handles.scrollbar,'Min',0);
set(handles.scrollbar,'Max',videoinfo.NumberOfFrame); 

% audio
set(handles.mute,'String','Mute');
[handles.y,handles.Fs]=audioread(videoinfo.Name);
handles.p = audioplayer(handles.y,handles.Fs);
handles.TotalSamples = handles.p.TotalSample; 
handles.Bstart = handles.TotalSamples/handles.NumberOfFrame;

% rgb
set(handles.Enable,'String','Disable');

% load the video at frame 1 and at stop
set(handles.info,'String',infomov);
set(handles.playpause,'String','Play');
    handles.CurrentFrame=1; %set the video file to 1 frame
    guidata(hObject,handles) % update the guidata
    frame = read(handles.videoinfo,handles.CurrentFrame); % Here we use the stored video position 
    image(frame,'Parent',handles.videobox);% Play the video on Axe
    image(frame,'Parent',handles.saturation);% Play the video on a separate axis for saturation
    image(frame,'Parent',handles.special);
    uiwait();
guidata(hObject, handles);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% PLAY & PAUSE FUNCTION %%%%%%%%%%%%%%%%%%%%%
function playpause_Callback(hObject, eventdata, handles)

if (strcmp(get(handles.playpause,'String'),'Play')) 
    set(handles.playpause,'String','Pause');

elseif (strcmp(get(handles.playpause,'String'),'Pause'))
    set(handles.playpause,'String','Play'); 
    pause(handles.p)
end
    
while(strcmp(get(handles.playpause,'String'),'Pause')) && handles.CurrentFrame<=handles.NumberOfFrame 
         handles.CurrentFrame = handles.CurrentFrame + 1;
         frame = read(handles.videoinfo,handles.CurrentFrame);
         image(frame,'Parent',handles.videobox);

        if (strcmp(get(handles.Enable,'String'),'Disable')) ;
            redLayer = frame(:,:,1);
            greenLayer = frame(:,:,2);
            blueLayer = frame(:,:,3);
            [red, x] = imhist(redLayer);
            [green, x] = imhist(greenLayer);
            [blue, x] = imhist(blueLayer);
            axes(handles.special);
            plot(x,red, 'Red', x,green,'Green',x,blue,'Blue');
        elseif(strcmp(get(handles.Enable,'String'),'Enable')) 
            y=0;
            axes(handles.special)
            plot(y)
        end
        %audio MUTE
         if (strcmp(get(handles.mute,'String'),'Mute'));
            handles.start = handles.Bstart * handles.CurrentFrame;
            play(handles.p,[handles.start,handles.TotalSamples]) 
         elseif (strcmp(get(handles.mute,'String'),'Unmute'));
             pause(handles.p)
         end    
         
         %scroll bar
         set(handles.scrollbar,'Value', handles.CurrentFrame);
         guidata(hObject,handles);
         
         %saturation
         redAdd=get(handles.red,'Value');
         redScalar=1+redAdd;
         
         blueAdd=get(handles.blue,'Value');
         blueScalar=1+blueAdd;
         
         greenAdd=get(handles.green,'Value');
         greenScalar=1+greenAdd;
         
         % adjusted frame
         adjustedframe=frame;
         adjustedframe(:,:,1)=frame(:,:,1)*redScalar;
         adjustedframe(:,:,2)=frame(:,:,2)*blueScalar;
         adjustedframe(:,:,3)=frame(:,:,3)*greenScalar;
         
         % display saturation on axes
         image(adjustedframe,'Parent',handles.saturation);
         guidata(hObject,handles);
         drawnow;
end
     guidata(hObject,handles);
 
guidata(hObject,handles);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% STOP FUNCTION %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function stop_Callback(hObject, eventdata, handles)
  set(handles.playpause,'String','Play');
    stop(handles.p)
    handles.CurrentFrame=1;
    set(handles.scrollbar,'Value',handles.CurrentFrame);
    guidata(hObject,handles) % update the guidata
    frame = read(handles.videoinfo,handles.CurrentFrame); % Here we use the stored video position 
    image(frame,'Parent',handles.videobox);% Play the video on Axe
    uiwait();
 guidata(hObject,handles) % update the guidata


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% STEP FOWARD FUNCTION %%%%%%%%%%%%%%%%%%%%%%
function stepfoward_Callback(hObject, eventdata, handles)
if get(hObject,'Value')
    handles.CurrentFrame=handles.CurrentFrame+1;     % Increment the stored position
    frame = read(handles.videoinfo,handles.CurrentFrame); % Here we use the stored video position 
    image(frame,'Parent',handles.videobox);% Play the video on Axe
    drawnow;
    set(handles.scrollbar,'Value',handles.CurrentFrame);
    guidata(hObject,handles)
end
guidata(hObject,handles) % update the guidata


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% STEP BACK FUNCTION %%%%%%%%%%%%%%%%%%%%%%%%
function stepback_Callback(hObject, eventdata, handles)
if get(hObject,'Value')
    handles.CurrentFrame=handles.CurrentFrame-1;     % Increment the stored position
    frame = read(handles.videoinfo,handles.CurrentFrame); % Here we use the stored video position 
    image(frame,'Parent',handles.videobox);% Play the video on Axe
    drawnow;
    set(handles.scrollbar,'Value',handles.CurrentFrame);
    guidata(hObject,handles)
end
guidata(hObject,handles) % update the guidata


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% SLIDER FUNCTION %%%%%%%%%%%%%%%%%%%%%%%%%%%
function scrollbar_Callback(hObject, eventdata, handles)
if get(hObject,'Value')
    set(handles.playpause,'String','Play');
    sliderValue = get(handles.scrollbar,'Value');
    handles.CurrentFrame=sliderValue;     % Increment the stored position
    frame = read(handles.videoinfo,handles.CurrentFrame); % Here we use the stored video position 
    image(frame,'Parent',handles.videobox);% Play the video on Axe
    drawnow;
    guidata(hObject,handles)
end
guidata(hObject, handles)

% %%%%%%%%%%%%%%%%%%%%%%%%%%%%% MUTE FUNCTION %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function mute_Callback(hObject, eventdata, handles)
if (strcmp(get(handles.mute,'String'),'Unmute')) 
    set(handles.mute,'String','Mute'); 
elseif (strcmp(get(handles.mute,'String'),'Mute'))
    set(handles.mute,'String','Unmute');
end
guidata(hObject,handles);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% ENABLE FUNCTION %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function Enable_Callback(hObject, eventdata, handles)
if (strcmp(get(handles.Enable,'String'),'Disable')) 
    set(handles.Enable,'String','Enable');
elseif (strcmp(get(handles.Enable,'String'),'Enable'))
    set(handles.Enable,'String','Disable'); 
end
guidata(hObject,handles);
