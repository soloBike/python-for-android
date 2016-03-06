package org.kivy.android;

import java.io.File;

import android.util.Log;
import java.lang.System;


public class PythonUtil {
	private static final String TAG = "PythonUtil";

	protected static String[] getLibraries() {
        return new String[] {
            "SDL2",
            "SDL2_image",
            "SDL2_mixer",
            "SDL2_ttf",
			"python2.7",
			"gnustl_shared",
			"zmq",
            "main"
        };
    }

	public static void loadLibraries(File filesDir) {

        String filesDirPath = filesDir.getAbsolutePath();
		Log.v(TAG, "LD_LIBRARY_PATH is " + System.getenv("LD_LIBRARY_PATH"));

		for (String lib : getLibraries()) {
			Log.v(TAG, "Load library:" + lib);
            System.loadLibrary(lib);
        }

        try {
            System.loadLibrary("python2.7");
        } catch(UnsatisfiedLinkError e) {
            Log.v(TAG, "Failed to load libpython2.7");
        }

        try {
            System.loadLibrary("python3.5m");
        } catch(UnsatisfiedLinkError e) {
            Log.v(TAG, "Failed to load libpython3.5m");
        }

        try {
            System.load(filesDirPath + "/lib/python2.7/lib-dynload/_io.so");
            System.load(filesDirPath + "/lib/python2.7/lib-dynload/unicodedata.so");
        } catch(UnsatisfiedLinkError e) {
            Log.v(TAG, "Failed to load _io.so or unicodedata.so...but that's okay.");
        }

        try {
            // System.loadLibrary("ctypes");
            System.load(filesDirPath + "/lib/python2.7/lib-dynload/_ctypes.so");
        } catch(UnsatisfiedLinkError e) {
            Log.v(TAG, "Unsatisfied linker when loading ctypes");
        }

        Log.v(TAG, "Loaded everything!");
	}
}
