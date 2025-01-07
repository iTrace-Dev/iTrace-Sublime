# iTrace-Sublime
iTrace-Sublime is a plugin for the Sublime Text Editor. The plugin will establish a connection to the [iTrace-Core](https://github.com/iTrace-Dev/iTrace-Core) desktop application. Once connected to the Core, the plugin will accept eye-tracking information from the Core and translate it to editor-specific data and output said data to an XML file.

# Installation
1. Download or clone the repository.
2. Navigate to your Sublime's Packages folder. Typically this is `/<User>/AppData/Roaming/Sublime Text/Packages/`. You can also get there by selecting Preferences->Browse Packages...
3. Copy the downloaded folder into the Packages folder.
4. Open Sublime. The plugin should now be installed.

# Usage
To use iTrace-Sublime, make sure you have iTrace-Core installed.
1. Open any files or folders you wish to view in Sublime.
2. Run iTrace-Core and set up the parameters of your tracking session.
3. Press `Ctrl+Shift+P`. This will open up the command palette.
4. Type "iTrace" to see the available commands. Select iTrace: Connect to Core.
5. iTrace-Sublime should now be connected to iTrace-Core. To check, you can press Ctrl+` to check the console output.
6. Once a tracking session is started, iTrace-Sublime will begin writing to a file in the location specified in iTrace-Core. When the tracking session is finished, two files will be present - one from iTrace-Sublime and the other from iTrace-Core.

# Further Steps
After gathering your data, you can use our other tools [iTrace-Toolkit](https://github.com/iTrace-Dev/iTrace-Toolkit) and [iTrace-Visualize](https://github.com/iTrace-Dev/iTrace-Visualize) to analyze and process the tracking sessions.
