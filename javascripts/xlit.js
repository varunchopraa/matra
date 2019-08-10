/*

  Author: Varun Chopra
  Date of completion: 26/07/2019
  Description: This is the JavaScript file responsible for making the interaction between the web page and the python script work through an AJAX call.

*/

$(document).ready(function(){

  //Pasted string
  document.getElementById("inp").onpaste = function(e){
      console.log("inp after pasting: " + document.getElementById("inp").value);

      var pastedText = undefined;
      if (window.clipboardData && window.clipboardData.getData) { //for IE
        pastedText = window.clipboardData.getData('Text');
      } 
      else if (e.clipboardData && e.clipboardData.getData) {
        pastedText = e.clipboardData.getData('text/plain');
      }
      //alert(pastedText); // Process and handle text...
      document.getElementById("inp").value += pastedText;
      //return false; // Prevent the default handler from running.
      querystring = $("form").serialize();
      var flag = 'True';
      xlit(querystring, flag);                    
      return false;
    };

  //Real time input
  $("textarea").keyup(function(e){
    if(e.keyCode == 32 || e.keyCode == 13 || (e.keyCode >= 186 && e.keyCode <=191)){
      querystring = $("form").serialize();
      var flag = 'False';
      xlit(querystring, flag);                    
    }
  });
});

//AJAX call to _transliterate() function present in transliterate.py hosted on same server at ../transliterate
function xlit(querystring, flag){

  var qs = '';
  qs = qs.concat('flag=', flag, '&', querystring)
  console.log("querystring: " + qs);
  var request = $.ajax({
    method: "GET",
    contentType: "json",
    url: '/transliterate?' + qs
  });
  request.done(function(response) {
    var x = document.getElementById("inp");
    response = JSON.parse(response);
    //Real time transliteration
    x.value = response.itrans;
    //Passing list of options to Autocomplete widget
    suggest(response.options);
  });
}

//jQuery Autocomplete Widget
function suggest(opt){
  $( function() {
    var availableTags = opt;
    console.log(availableTags);

    function split( val ) {
      return val.split( / \s*/ );
    }
    function extractLast( term ) {
      return split( term ).pop();
    }
    //change inp to custom tag id
    $( "#inp" )
      .on( "keydown", function( event ) {
        if ( event.keyCode === $.ui.keyCode.TAB &&
            $( this ).autocomplete( "instance" ).menu.active ) {
              event.preventDefault();
        }
      })
      .autocomplete({
        minLength: 0,
        source: function( request, response ) {
          response( $.ui.autocomplete.filter(
            availableTags, extractLast( request.term ) ) );
        },
        focus: function() {
          return false;
        },
        select: function( event, ui ) {
          var terms = split( this.value );
          // remove the current input
          terms.pop();
          terms.pop();
          // add the selected item
          terms.push( ui.item.value );
          // add placeholder to get the space at the end
          terms.push( "" );
          this.value = terms.join( " " );
          return false;
        }
      })
      //invoked on space
      .on("keyup"), function(e){
        if(e.keyCode == 32){
          $(this).autocomplete("search", "");
        }
      };
  });
}