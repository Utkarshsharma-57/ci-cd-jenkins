from flask import Flask

# Flask Constructor
app = Flask(__name__)

# decorator to associate 
# a function with the url
@app.route("/")
def showHomePage():
      # response from the server
    return "This is home page"

if __name__ == "__main__":
  app.run(host="0.0.0.0")<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout 
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@color/white"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/pagename"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_marginStart="12dp"
        android:layout_marginEnd="12dp"
        android:textAlignment="center"
        android:textColor="@color/black"
        android:textSize="16sp"
        android:textStyle="bold"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />
    
</androidx.constraintlayout.widget.ConstraintLayout>import android.os.Bundle;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.jetbrains.annotations.NotNull;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {
    
    // declare attribute for textview
    private TextView pagenameTextView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        pagenameTextView = findViewById(R.id.pagename);

        // creating a client
        OkHttpClient okHttpClient = new OkHttpClient();

        // building a request
        Request request = new Request.Builder().url("http://192.168.0.113:5000/").build();

        // making call asynchronously
        okHttpClient.newCall(request).enqueue(new Callback() {
            @Override
            // called if server is unreachable
            public void onFailure(@NotNull Call call, @NotNull IOException e) {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        Toast.makeText(MainActivity.this, "server down", Toast.LENGTH_SHORT).show();
                        pagenameTextView.setText("error connecting to the server");
                    }
                });
            }

            @Override
            // called if we get a 
            // response from the server
            public void onResponse(
                    @NotNull Call call,
                    @NotNull Response response)
                    throws IOException {pagenameTextView.setText(response.body().string());
            }
        });
    }
}from flask import Flask

# import request
from flask import request
app = Flask(__name__)

@app.route("/")
def showHomePage():
    return "This is home page"

@app.route("/debug", methods=["POST"])
def debug():
    text = request.form["sample"]
    print(text)
    return "received"  
  
if __name__ == "__main__":
  app.run(host="0.0.0.0")<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout 
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@color/white"
    tools:context=".DummyActivity">

    <EditText
        android:id="@+id/dummy_text"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginStart="12dp"
        android:layout_marginEnd="12dp"
        android:backgroundTint="@color/black"
        android:hint="enter any text"
        android:textColor="@color/black"
        android:textColorHint="#80000000"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <Button
        android:id="@+id/dummy_send"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Send"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/dummy_text"
        app:layout_constraintVertical_bias="0.1" />

</androidx.constraintlayout.widget.ConstraintLayout>import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.jetbrains.annotations.NotNull;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class DummyActivity extends AppCompatActivity {

    private EditText editText;
    private Button button;
    private OkHttpClient okHttpClient;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_dummy);
        editText = findViewById(R.id.dummy_text);
        button = findViewById(R.id.dummy_send);
        okHttpClient = new OkHttpClient();

        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                
                String dummyText = editText.getText().toString();

                // we add the information we want to send in
                // a form. each string we want to send should
                // have a name. in our case we sent the
                // dummyText with a name 'sample'
                RequestBody formbody
                        = new FormBody.Builder()
                        .add("sample", dummyText)
                        .build();

                // while building request
                // we give our form
                // as a parameter to post()
                Request request = new Request.Builder().url("http://192.168.0.113:5000/debug")
                        .post(formbody)
                        .build();
                okHttpClient.newCall(request).enqueue(new Callback() {
                    @Override
                    public void onFailure(
                            @NotNull Call call,
                            @NotNull IOException e) {
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                Toast.makeText(getApplicationContext(), "server down", Toast.LENGTH_SHORT).show();
                            }
                        });
                    }

                    @Override
                    public void onResponse(@NotNull Call call, @NotNull Response response) throws IOException {
                        if (response.body().string().equals("received")) {
                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    Toast.makeText(getApplicationContext(), "data received", Toast.LENGTH_SHORT).show();
                                }
                            });
                        }
                    }
                });
            }
        });
    }
}
