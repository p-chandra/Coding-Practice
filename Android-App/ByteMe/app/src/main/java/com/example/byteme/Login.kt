package com.example.byteme

import android.content.Intent
import android.os.Bundle
import android.support.v7.app.AlertDialog
import android.support.v7.app.AppCompatActivity
import android.widget.TextView
import android.widget.Toast
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.FirebaseAuthException
import com.google.firebase.auth.FirebaseUser
import kotlinx.android.synthetic.main.activity_login.*


class Login : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        login_signup_btn.setOnClickListener{
            val intent = Intent(this, SignUP::class.java)
                startActivity(intent)
        }
        login_signin_btn.setOnClickListener{
            userValidate()
        }
        val link = findViewById(R.id.login_help) as TextView
        link.setOnClickListener {
            popUp()
        }
    }

    private fun userValidate(){
        val email = login_email.text.toString().trim()
        val password = login_password.text.toString()
        var auth = FirebaseAuth.getInstance()
        if (email.isEmpty() || password.isEmpty()){
            Toast.makeText(this@Login, "Empty Text Field", Toast.LENGTH_SHORT).show()
        }
        else {
            auth.signInWithEmailAndPassword(email, password)
                .addOnCompleteListener {
                    if(it.isSuccessful) {
                        val firebaseUser = it.result?.user
                        val emailVerified = firebaseUser!!.isEmailVerified
                        if(!emailVerified){
                            Toast.makeText(this@Login,"Email is not Verified", Toast.LENGTH_SHORT).show()
                        }else {
                            //Do something here
                            Toast.makeText(this@Login, "Logging in", Toast.LENGTH_SHORT).show()
                            //val intent = Intent(this, Select::class.java)
                            //startActivity(intent)
                        }
                    }else{
                        val e = it.getException() as FirebaseAuthException
                        //Toast.makeText(this@Login, "Error " + e.message, Toast.LENGTH_SHORT).show()
                        Toast.makeText(this@Login, "Invalid Credentials ", Toast.LENGTH_SHORT).show()
                    }
                }
        }
    }

    private fun popUp(){
        val builder = AlertDialog.Builder(this)
        builder.setTitle("Trouble?")
        builder.setMessage("\nMake sure you are using your school email\n\nNew here? sign up now")

        builder.setPositiveButton("Reset"){dialog, which ->
            Toast.makeText(applicationContext, "Email sent with new password", Toast.LENGTH_SHORT)
                        .show()
        }
        builder.setNegativeButton("Sign up"){dialog,which ->
            Toast.makeText(applicationContext,"Signing Up..",Toast.LENGTH_SHORT).show()
        }
        builder.setNeutralButton("Cancel"){_,_ ->
            Toast.makeText(applicationContext,"Cancelled",Toast.LENGTH_SHORT).show()
        }
        val dialog: AlertDialog = builder.create()

        // Display the alert dialog on app interface
        dialog.show()

    }
}
