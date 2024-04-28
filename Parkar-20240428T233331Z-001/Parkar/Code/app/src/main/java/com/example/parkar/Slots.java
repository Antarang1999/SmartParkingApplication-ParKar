package com.example.parkar;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.ListView;

public class Slots extends AppCompatActivity {
    ListView slot;
    String[] places={"MangalWari","Haldiram Hotspot","Azad Chowk","VCA Complex "};
    Intent place;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_slots);
         slot=(ListView)findViewById(R.id.slot);
         slot.setAdapter(new ArrayAdapter<String>(this,android.R.layout.simple_dropdown_item_1line,places));
         place=new Intent(this,DisplaySlot.class);
         startActivity(place);

    }
}
