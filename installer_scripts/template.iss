#define PROGRAMNAME "Ink/Stitch"
;inkstitch-version
#define AppId "org.inkstitch.app"
#define AppDescription "InkStitch: an Inkscape extension for machine embroidery design."
#define AppPublisher "InkStitch Open Source Community"
#define URL "https://inkstitch.org/"
;inkstitch-year
#define PATHTODIST "..\dist"
#define INXPATH "..\inx"
[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)

LanguageDetectionMethod=uilanguage
;AppId={{C78E6C6F-C47E-4319-AF5A-E71387AE2D4E}
AppId={#AppId}
AppName={#PROGRAMNAME}
AppVersion={#VERSION}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisherURL={#URL}
AppSupportURL={#URL}
AppUpdatesURL={#URL}
DefaultDirName={userappdata}\inkscape\extensions\
DefaultGroupName={#PROGRAMNAME}
; Remove the following line to run in administrative install mode (install for all users.)
PrivilegesRequired=lowest
OutputBaseFilename=inkstitch
;arch-allowed
OutputDir=.
Compression=lzma
SolidCompression=yes
VersionInfoCompany={#URL}
VersionInfoCopyright=Copyright (C) {#COPYRIGHT}
VersionInfoDescription={#AppDescription}
VersionInfoTextVersion={#VERSION}
VersionInfoVersion=1.0
WizardStyle=modern
ShowLanguageDialog=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "armenian"; MessagesFile: "compiler:Languages\Armenian.isl"
Name: "brazilian"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "catalan"; MessagesFile: "compiler:Languages\Catalan.isl"
Name: "corsican"; MessagesFile: "compiler:Languages\Corsican.isl"
Name: "czech"; MessagesFile: "compiler:Languages\Czech.isl"
Name: "danish"; MessagesFile: "compiler:Languages\Danish.isl"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"
Name: "hebrew"; MessagesFile: "compiler:Languages\Hebrew.isl"
Name: "norwegian"; MessagesFile: "compiler:Languages\Norwegian.isl"
Name: "polish"; MessagesFile: "compiler:Languages\Polish.isl"
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "finnish"; MessagesFile: "compiler:Languages\Finnish.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"
Name: "dutch"; MessagesFile: "compiler:Languages\Dutch.isl"
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "slovak"; MessagesFile: "compiler:Languages\Slovak.isl"
Name: "slovenian"; MessagesFile: "compiler:Languages\Slovenian.isl"
Name: "turkish"; MessagesFile: "compiler:Languages\Turkish.isl"
Name: "ukrainian"; MessagesFile: "compiler:Languages\Ukrainian.isl"

[Types]
Name: "English"; Description: "English";

[Files]
Source: "{#PATHTODIST}\inkstitch\*"; DestDir: "{app}\inkstitch\inkstitch"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files 
[Code]
// SOURCE: https://stackoverflow.com/questions/2000296/inno-setup-how-to-automatically-uninstall-previous-installed-version 
{ ///////////////////////////////////////////////////////////////////// }
function GetUninstallString(): String;
var
  sUnInstPath: String;
  sUnInstallString: String;
begin
  sUnInstPath := ExpandConstant('Software\Microsoft\Windows\CurrentVersion\Uninstall\{#emit SetupSetting("AppId")}_is1');
  sUnInstallString := '';
  if not RegQueryStringValue(HKLM, sUnInstPath, 'UninstallString', sUnInstallString) then
    RegQueryStringValue(HKCU, sUnInstPath, 'UninstallString', sUnInstallString);
  Result := sUnInstallString;
end;


{ ///////////////////////////////////////////////////////////////////// }
function IsUpgrade(): Boolean;
begin
  Result := (GetUninstallString() <> '');
end;


{ ///////////////////////////////////////////////////////////////////// }
function UnInstallOldVersion(): Integer;
var
  sUnInstallString: String;
  iResultCode: Integer;
begin
{ Return Values: }
{ 1 - uninstall string is empty }
{ 2 - error executing the UnInstallString }
{ 3 - successfully executed the UnInstallString }

  { default return value }
  Result := 0;

  { get the uninstall string of the old app }
  sUnInstallString := GetUninstallString();
  if sUnInstallString <> '' then begin
    sUnInstallString := RemoveQuotes(sUnInstallString);
    if Exec(sUnInstallString, '/SILENT /NORESTART /SUPPRESSMSGBOXES','', SW_HIDE, ewWaitUntilTerminated, iResultCode) then
      Result := 3
    else
      Result := 2;
  end else
    Result := 1;
end;

{ ///////////////////////////////////////////////////////////////////// }
function InitializeSetup(): Boolean;
var
  UserExtensionsPath: String;
  UserInkscapePath: String;
  ProgramFilesExtPath: String;
begin
  Result := True;
  
  // Standard user extensions path (works for both traditional and MS Store installations)
  UserExtensionsPath := ExpandConstant('{userappdata}\inkscape\extensions\');
  UserInkscapePath := ExpandConstant('{userappdata}\inkscape\');
  
  // Alternative: Program Files path (traditional .exe installation)
  ProgramFilesExtPath := ExpandConstant('{commonpf}\Inkscape\share\inkscape\extensions\');

  // Check if user extensions folder exists
  if DirExists(UserExtensionsPath) then
  begin
    Log('Found Inkscape user extensions folder');
    Exit;
  end;
  
  // Check Program Files path as alternative indicator that Inkscape is installed
  if DirExists(ProgramFilesExtPath) then
  begin
    Log('Found Inkscape in Program Files, creating user extensions folder');
  end
  else
  begin
    // Neither path exists - Inkscape might not be installed
    Log('No Inkscape installation detected');
  end;
  
  // Try to create the user extensions folder (the standard location for user extensions)
  // First create inkscape folder if needed
  if not DirExists(UserInkscapePath) then
  begin
    if not ForceDirectories(UserInkscapePath) then
    begin
      MsgBox('Error: Could not create Inkscape configuration folder.' + #13#10 + #13#10 +
             'Please install and run Inkscape at least once, then try again.' + #13#10 + #13#10 +
             'Path: ' + UserInkscapePath, mbError, MB_OK);
      Result := False;
      Exit;
    end;
  end;
  
  // Now create extensions folder
  if not ForceDirectories(UserExtensionsPath) then
  begin
    MsgBox('Error: Could not create extensions folder.' + #13#10 + #13#10 +
           'Please create this folder manually and try again:' + #13#10 +
           UserExtensionsPath, mbError, MB_OK);
    Result := False;
    Exit;
  end;
  
  Log('Successfully created Inkscape extensions folder');
end;

{ ///////////////////////////////////////////////////////////////////// }
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if (CurStep=ssInstall) then
  begin
    if (IsUpgrade()) then
    begin
      UnInstallOldVersion();
    end;
  end;
end;
