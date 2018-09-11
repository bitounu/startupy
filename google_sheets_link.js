// upload document into google spreadsheet
    // and put link to it into current cell

    function onOpen(e) {
      var ss = SpreadsheetApp.getActiveSpreadsheet()
      var menuEntries = [];
      menuEntries.push({name: "File...", functionName: "doGet"});
      ss.addMenu("Attach ...", menuEntries);
    }

    function doGet(e) {
      var app = UiApp.createApplication().setTitle("upload attachment into Google Drive");
      SpreadsheetApp.getActiveSpreadsheet().show(app);
      var form = app.createFormPanel().setId('frm').setEncoding('multipart/form-data');
      var formContent = app.createVerticalPanel();
      form.add(formContent);  
      formContent.add(app.createFileUpload().setName('thefile'));

      // these parameters need to be passed by form
      // in doPost() these cannot be found out anymore
      formContent.add(app.createHidden("activeCell", SpreadsheetApp.getActiveRange().getA1Notation()));
      formContent.add(app.createHidden("activeSheet", SpreadsheetApp.getActiveSheet().getName()));
      formContent.add(app.createHidden("activeSpreadsheet", SpreadsheetApp.getActiveSpreadsheet().getId()));
      formContent.add(app.createSubmitButton('Submit'));
      app.add(form);
      SpreadsheetApp.getActiveSpreadsheet().show(app);
      return app;
    }

    function doPost(e) {
      var app = UiApp.getActiveApplication();
      app.createLabel('saving...');
      var fileBlob = e.parameter.thefile;
  var doc = DriveApp.getFolderById('0B-pKUwYk4W5GV3JpTC16UVNURDg').createFile(fileBlob);
      var label = app.createLabel('file uploaded successfully');

      // write value into current cell
      var value = 'hyperlink("' + doc.getUrl() + '";"' + doc.getName() + '")'
      var activeSpreadsheet = e.parameter.activeSpreadsheet;
      var activeSheet = e.parameter.activeSheet;
      var activeCell = e.parameter.activeCell;
      var label = app.createLabel('file uploaded successfully');
      app.add(label);
      SpreadsheetApp.openById(activeSpreadsheet).getSheetByName(activeSheet).getRange(activeCell).setFormula(value);
      app.close();
      return app;
    }
