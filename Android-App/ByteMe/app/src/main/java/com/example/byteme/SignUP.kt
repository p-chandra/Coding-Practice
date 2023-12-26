package com.example.byteme

import android.app.AlertDialog
import android.content.Intent
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.widget.Toast
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.FirebaseAuthException
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.database.IgnoreExtraProperties
import kotlinx.android.synthetic.main.activity_sign_up.*
import android.os.Handler
import android.widget.TextView


open class SignUP : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?)
    {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_sign_up)

        signup_next.setOnClickListener {

            val email = signup_email.text.toString().trim()
            val password = signup_password.text.toString()
            val confirm_pass = signup_confirm_password.text.toString()
            val fname = signup_fname.text.toString().trim().toUpperCase()
            val lname = signup_lname.text.toString().trim().toUpperCase()

            /*
            boolean verifying. true if everything goes well
             */
            if (userValidate(email, password, confirm_pass, fname, lname))
            {
                Toast.makeText(this@SignUP, "Checking user credentials", Toast.LENGTH_SHORT).show()
                val database = FirebaseDatabase.getInstance().reference
                val myAuth = FirebaseAuth.getInstance()

                myAuth.createUserWithEmailAndPassword(email, password).addOnCompleteListener {
                    if (!it.isSuccessful) {
                        // Displays the error if any
                        val e = it.getException() as FirebaseAuthException
                        Toast.makeText(this@SignUP, "Error " + e.message, Toast.LENGTH_SHORT).show()
                    } else {
                        val userInformation = userData(fname, lname, email, password) //load information to database
                        database.child(fname).setValue(userInformation)
                        myAuth.currentUser?.sendEmailVerification()?.addOnCompleteListener {
                            if (it.isSuccessful) {
                                val intent = Intent(this, Login::class.java)
                                Toast.makeText(this@SignUP, "Link has been sent", Toast.LENGTH_SHORT).show()
                                startActivity(intent)
                            } else {
                                val e = it.getException() as FirebaseAuthException
                                Toast.makeText(this@SignUP, "Error " + e.message, Toast.LENGTH_SHORT).show()
                            }
                        }
                    }
                }
            }
        }
    }


    private fun userValidate(email: String, password: String, confirm_pass: String,
        fname: String, lname: String): Boolean {

        if (!email.isEmpty() && !password.isEmpty() && !fname.isEmpty() && !lname.isEmpty() && !confirm_pass.isEmpty()) {
            if (password.length >= 6) {
                if (password == confirm_pass) {
                    return true
                } else Toast.makeText(this@SignUP, "Password does not match", Toast.LENGTH_SHORT).show()
            } else Toast.makeText(this@SignUP, "Password must be at least 6 characters long", Toast.LENGTH_SHORT).show()
        } else Toast.makeText(this@SignUP, "Empty Field", Toast.LENGTH_SHORT).show()
        return false
    }

    @IgnoreExtraProperties
    data class userData(
        var fname: String? = "",
        var lname: String? = "",
        var email: String? = "",
        var password: String? = ""
    )
}