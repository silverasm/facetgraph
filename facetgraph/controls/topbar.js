/*
	Author: Aditi Muralidharan
*/

function displayTopBar(data) {
	$('#topbar').ajaxForm({
		dataType: 'json',
		success: drawGraph,
		url: data.action,
		type:"GET"
	});
	
	// Insert the form's content
	for(var i = 0; i < data.inputs.length; i++){
		$('#topbar').append(makeFormLabel(data.inputs[i]));
		$('#topbar').append(makeFormInput(data.inputs[i]));
	}

	for(var k = 0; k < data.inputs.length; k++){
		if(data.inputs[k].type =="text"){
			input = data.inputs[k];
			if(input.autocomplete){
				var options = { 
				serviceUrl:autoCompleteURL,
				minChars:0, 
				delimiter: /(,|;)\s*/, // regex or character
				maxHeight:400,
				width:300,
				zIndex: 9999,
				deferRequestBy: 0, //miliseconds
				noCache: true //default is false, set to true to disable caching
			  };
			  var id = "#"+input.name;
			  autocomplete = $(id).autocomplete(options);

			}else{
			  $("#debug").html("hi");

			}
		}
	}
	
	// set the autocomplete parameters on a click
	for(var n = 0; n < data.inputs.length; n++){
		if(data.inputs[n].inform_autocomplete =="true"){
			var input = data.inputs[n];
			var id = "#"+input.name;
			var formID = "#topbar :"+input.name;
			var value = $(id).click(function(){
				var val = $("#topbar")[0][input.name].value;
				autocomplete.setOptions({params: {type:val} });
			});
		}
	}
};



function makeFormLabel(input){
	if(input.label){
		return "<label>"+input.label+"</label>"
	}
}

function makeFormInput(input){
	params = input.parameters;
	if(input.type == "select"){
		html = "<select "
		html += ' id="'+input.name+'"'
		html += ' name="'+input.name+'">'
		for(var j = 0; j < params.options.length; j++){
			option = params.options[j];
			if(option.selected == "selected"){
				html += '<option selected="selected"'
			}else{
				html += "<option "
			}
			html += 'value="'+option.value+'">'
			html += option.text
			html += "</option>"
		}
		html += "</select>"
	}else if(input.type == "number"){
		html = '<input type="number"'
		html += ' name="'+input.name+'"'
		if(params.min){
			html += ' min="'+params.min+'"'
		}
		if(params.max){
			html += ' max="'+params.max+'"'
		}
		if(params.step){
			html += ' step="'+params.step+'"'
		}
		if(params.value){
			html += ' value="'+params.value+'"'
		}
		html += ">"		
	}else if(input.type == "text"){
		html = '<input type="text"'
		html += ' name="'+input.name+'"'
		html += ' id="'+input.name+'"'
		if(params.value){
			html += ' value="'+params.value+'"'
		}
		html += ">"	
	}else if(input.type == "submit"){
		html = '<input type="submit" value="'+params.value+'" />'
	}else{
		html = ""
	}
	return html
}