
function show_json(response){

	deb(formattedJSON(response));
}



// Create namespace object to avoid collisions.
var org;
if (!org) {
	org = {};
}
if (!org.bibkn) {
	org.bibkn = {};
}
if (!org.bibkn.Dataset) {
	org.bibkn.Dataset = {};
}



org.bibkn.Dataset.json_file_req = function(){
	// Test if IE and allow support for versions of IE before 7.
	if (window.ActiveXObject){
		try {
			return new ActiveXObject("Msxml2.XMLHTTP");
		} catch (exception) {
			//Silence error.
		}
		try {
			return new ActiveXObject("Microsoft.XMLHTTP");
		} catch (exception) {
			//Silence error.
		}
	} else {
		// Everyone else (Firefox, Safari, Chrome, etc.)
		if (window.XMLHttpRequest) {
			return new XMLHttpRequest();
		} else {
			return false;
		}
	}
}


org.bibkn.Dataset.load = function() {
	var Dataset = org.bibkn.Dataset;
	// XMLHttpRequest object.
	var jsonRequest = new Dataset.json_file_req();

	// On state change, load information. So when info is loaded into request or request is sent.
	jsonRequest.onreadystatechange= function() {
		// Check all data of request has been received.
		if (jsonRequest.readyState==4){
			// Check http response status is OK (200).
			if (jsonRequest.status==200 || window.location.href.indexOf("http")==-1){
				// Convert request(json) to javascript object.
				var jsondata = eval("("+jsonRequest.responseText+")");
				Dataset.datasets = jsondata.recordList;
				Dataset.schema = jsondata.dataset.table_cols;
				Dataset.reorder(Dataset.schema[0],'ascending');
			} else {
				alert("Error; something went wrong with the request.");
			}
		}
	}

	jsonRequest.open("GET", "dod.bib.json", true);
	jsonRequest.send();
}

org.bibkn.Dataset.reorder = function(topic, ordering, record_num, property, pg_num, num_pp) {
	var Dataset = org.bibkn.Dataset;
	var output = '<table class="data_table">';

	if (topic == undefined) {
		topic = Dataset.schema[0];
	}
	if (ordering == undefined) {
		ordering = 'ascending';
	}
	if (record_num == undefined) {
		record_num = -1;
	}
	if (property == undefined) {
		property = null;
	}
	if (pg_num == undefined || pg_num < 0) {
		pg_num = 0;
	}
	if (num_pp == undefined) {
		num_pp = 25; //5; //changed by Jack Alves
	}

	output += '<col id="col1"><col id="col2"><col id="col3"><col id="col4"><tr>';

	for (var c = 0; c < Dataset.schema.length; c++) {
		if (topic == Dataset.schema[c]) {
			if (ordering == 'ascending') {
				output += '<th class="data_header" id="selected_des" onmousedown="org.bibkn.Dataset.reorder(\'' + Dataset.schema[c] + '\', \'descending\');"><u>' + Dataset.display(Dataset.schema[c]) + '</u></th>';
			} else {
				output += '<th class="data_header" id="selected_asc" onmousedown="org.bibkn.Dataset.reorder(\'' + Dataset.schema[c] + '\', \'ascending\');"><u>' + Dataset.display(Dataset.schema[c]) + '</u></th>';
			}
		} else {
			output += '<th class="data_header" onmousedown="org.bibkn.Dataset.reorder(\'' + Dataset.schema[c] + '\', \'ascending\');">' + Dataset.display(Dataset.schema[c]) + '</th>';
		}
	}
	output += '</tr>';

	if (topic == 'size' || topic == 'records') {
		if (ordering == 'ascending') {
			Dataset.datasets = Dataset.datasets.sort(function(a,b) {return a[topic] > b[topic];});
		} else {
			Dataset.datasets = Dataset.datasets.sort(function(a,b) {return a[topic] < b[topic];});
		}
	} else {
		if (ordering == 'ascending') {
			Dataset.datasets = Dataset.datasets.sort(function(a,b) {return (a[topic]+"").substring(0,1).toLowerCase() > (b[topic]+"").substring(0,1).toLowerCase();});
		} else {
			Dataset.datasets = Dataset.datasets.sort(function(a,b) {return (a[topic]+"").substring(0,1).toLowerCase() < (b[topic]+"").substring(0,1).toLowerCase();});
		}
	}

	for (var i = pg_num*num_pp; i < Dataset.datasets.length && i < pg_num*num_pp+num_pp; i++){
		output+='<tr>';

		for (var x=0; x < Dataset.schema.length; x++) {
			var prop = Dataset.schema[x];
			if (prop == 'description') {
				output += '<td class="data_entry' + i%2 + '" id="td_descript">';
//				output += '<table>'
				for (var other_properties in Dataset.datasets[i]) {
					if (other_properties != 'name' && other_properties !='size' && other_properties !='records') {						
						if (record_num == i && other_properties == property) {
							// modified by Jack Alves to simplify display
//							output += '<form><b>' + Dataset.display(other_properties) + ': </b>';
//							output +=  '<textarea rows=1>' + Dataset.datasets[record_num][property];
//							output +=  '</textarea><br>';
//							output +=  '<input type="submit" value="Change">&nbsp&nbsp';
//							output +=  '<button onmousedown="org.bibkn.Dataset.reorder(\'';
//							output +=   topic + '\',\'' + ordering + '\', undefined, undefined,' + pg_num + ',' + num_pp;
//							output +=  ')">Cancel</button>';
//							output += '</form>';
						} else {
//							output+='<b onmousedown="org.bibkn.Dataset.reorder(\'' + topic + '\',\'' + ordering + '\',' + i + ',\'' + other_properties + '\',' + pg_num + ',' + num_pp + ')">' + Dataset.display(other_properties) + ': </b>' + Dataset.display(Dataset.datasets[i][other_properties]) + '<br><br>';
//							other_properties = other_properties.toLowerCase();
							switch (other_properties) {
							// creator, source, createdDate, download, schema, browse
								case 'description':
									output += '<div class="other_prop">';
									output += other_properties;
									output += '</div>';
									output += '<div class="other_value">'
									output += Dataset.datasets[i][other_properties];
									output += '</div>';
									break;
								case 'collected':
									output += '<div>'; //'<tr>';
									output += '<span class="other_prop">';//'<td class="other_prop">';
									output += 'collected';//other_properties;
									output += '</span>'; //'</td>';				
									output += '<span class="other_value">';//'<td class="other_value">';
									output += Dataset.datasets[i][other_properties];
									output += '</span>'; //'</td>';				
									output += '</div>'; //'</tr>';
									break;
								case 'download':
								case 'browse':
									output += ''; //'<tr>';
									output += '<div class="other_prop">';//'<td class="other_value">';
									output += '<a href="'+ Dataset.datasets[i][other_properties]+'">' + other_properties +'</a>';
									output += '</div>'; //'</td>';				
									output += ''; //'</tr>';
									break;
								case 'schema':
									output += '<div>'; //'<tr>';
									output += '<span class="other_prop">';//'<td class="other_prop">';
									output += 'schema ';
									output += '</span>'; //'</td>';				
//									output += '<span class="other_value">';//'<td class="other_value">';
									var v = Dataset.datasets[i][other_properties];
									if ((typeof(v) === 'object') && (v instanceof Array)) {
										output += '<div class="other_list_horizontal">'; //'<tr>';
										for (var vx=0; vx < v.length; vx++) {
											if (v[vx] && (typeof v[vx] == 'string')) {
												var vf = ''
												var vf_index = v[vx].lastIndexOf('\/')+1;
												if (vf_index > 0) {
													vf = v[vx].substring(vf_index);													
												}
												output += '<span><a href="'+v[vx]+'">'+vf+'</a>     </span>';
//												output += '&nbsp;&nbsp;'
//												if (vf && (vf != 'bibjson_schema\.json') && 
//														(vf != 'identifiers\.json')) {
//													output += '<span><a href="'+v[vx]+'">'+vf+'</a></span>';
//													output += '&nbsp;&nbsp;&nbsp;'
//												}
											}			
										}
										output += '</div>'; //'<tr>';
									}
									else {
										output += v;
									}
//									output += '</span>'; //'</td>';				
									output += '</div>'; //'</tr>';
									break;
								case 'creator':
									break; // drop this from display
									output += '<div>'; //'<tr>';
									output += '<span class="other_prop">';//'<td class="other_prop">';
									output += 'creator ';
									output += '</span>'; //'</td>';				
									output += '<span class="other_value">';//'<td class="other_value">';
									var v = Dataset.datasets[i][other_properties];
									if (typeof(v) === 'object') {
										if ('name' in v) {
											output += v['name'];
										}
									}
									else {
										output += v;
									}
									output += '</span>'; //'</td>';				
									output += '</div>'; //'</tr>';
									break;
								case 'source':
									output += '<div>'; //'<tr>';
									output += '<span class="other_prop">';//'<td class="other_prop">';
									output += 'source    ';//other_properties;
									output += '</span>'; //'</td>';				
									output += '<span class="other_value">';//'<td class="other_value">';
									var v = Dataset.datasets[i][other_properties];
									if (typeof(v) === 'object') {
										if (v instanceof Array) {
											for (var vx=0; vx < v.length; vx++) {
												if (v[vx] && (typeof v[vx] == 'string')) {
													output += '<a href="'+v[vx] +'">'+v[vx]+'</a>';
//													output += '<div>'+v[vx]+'</div>';
												}			
											}
										}
										else {
											var v_url = null;
											if ('href' in v) {
												v_url = v['href'];
											}
											if ('url' in v) {
												v_url = v['url'];
											}
											
											if (v_url) {
												output += '<a href="'+v_url +'">';
												if ('name' in v) {
													output += v['name']+'</a>';													
												}
												else {
													output += v_url+'</a>';													
												}
											}
											else if ('name' in v) {
												output += v['name'];
											}
										}
									}
									else {
										output += '<a href="'+v +'">'+v+'</a>';
									}
									output += '</span>'; //'</td>';				
									output += '</div>'; //'</tr>';
									break;
									
								default:
									break;
								
							}
						}
					}
				}
//				output += '</table>'; // nested table for other properties
				output += '</td>';
			} else {
				if (record_num == i && prop == property) {
//					output+='<td class="data_entry' + i%2 + '"><form><textarea rows=1>' + Dataset.datasets[record_num][property] + '</textarea><br><input type="submit" value="Change">&nbsp&nbsp<button onmousedown="org.bibkn.Dataset.reorder(\'' + topic + '\',\'' + ordering + '\', undefined, undefined,' + pg_num + ',' + num_pp + ')">Cancel</button></form></td>';
					output+='<td class="data_entry' + i%2 + '">' + Dataset.datasets[record_num][property] + '</td>';
				} else {
					output+='<td class="data_entry' + i%2 + '" onmousedown="org.bibkn.Dataset.reorder(\'' + topic + '\',\'' + ordering + '\',' + i + ',\'' + prop + '\',' + pg_num + ',' + num_pp + ')">' + Dataset.display(Dataset.datasets[i][prop]) + '</td>';
				}
			}
		}

		output+='</tr>';
	}

	if (pg_num >= 0) {
		if (pg_num == 0) {
			output+='<tr><td class="page_num" colspan="'+Dataset.schema.length +'">Prev...';
		} else {
			output+='<tr><td class="page_num" colspan="'+Dataset.schema.length +'"><a class="valid_pg" onmousedown="org.bibkn.Dataset.reorder(\'' + topic + '\',\'' + ordering + '\','+record_num+',\''+property+'\','+(pg_num-1)+')">Prev...</a>';
		}
		if (pg_num < 3) {
			for (var p = 0; p < 5; p++) {
				if (p == pg_num) {
					output+='<a class="valid_pg" id="current_page" onmousedown="org.bibkn.Dataset.reorder(\'' + topic + '\',\'' + ordering + '\','+record_num+',\''+property+'\','+ p +')">'+ p +'</a>';
				} else {
					if (p*num_pp < Dataset.datasets.length) {
						output+='<a class="valid_pg" onmousedown="org.bibkn.Dataset.reorder(\'' + topic + '\',\'' + ordering + '\','+record_num+',\''+property+'\','+ p +')">'+ p +'</a>';
					}
				}
			}
		} else {
			for (var p = -2; p < 3; p++) {
				if (p == 0) {
					output+='<a class="valid_pg" id="current_page" onmousedown="org.bibkn.Dataset.reorder(\'' + topic + '\',\'' + ordering + '\','+record_num+',\''+property+'\','+ pg_num +')">'+ pg_num +'</a>';
				} else {
					if ((pg_num+p)*num_pp < Dataset.datasets.length) {
						output+='<a class="valid_pg" onmousedown="org.bibkn.Dataset.reorder(\'' + topic + '\',\'' + ordering + '\','+record_num+',\''+property+'\','+ (pg_num+p) +')">'+ (pg_num+p) +'</a>';
					}
				}
			}
		}
		if ((pg_num+1)*num_pp < Dataset.datasets.length) {
			output+='<a class="valid_pg" onmousedown="org.bibkn.Dataset.reorder(\'' + topic + '\',\'' + ordering + '\','+record_num+',\''+property+'\','+(pg_num+1)+')">...Next</a></td></tr></table>';
		} else {
			output+='...Next</td></tr></table>';
		}
	} else {
		alert("Page numbering has failed.");
	}

	document.getElementById("request").innerHTML=output;
}

org.bibkn.Dataset.display = function(property) {
	var output = '';
	var url = /http/;
	var display;
	if (property instanceof Array) {
		for (var i = 0; i < property.length; i++) {
			if (i != (property.length-1)) {
				if (url.exec(property[i])) {
					display = property[i].split('/');
					if (parseFloat(display[display.length-1]) == parseInt(display[display.length-1])) {
						output += '<a href="' + property[i] + '">' + display[display.length-1] + '</a>, ';
					} else {
						output += '<a href="' + property[i] + '">' + display[display.length-1].substr(0,1).toUpperCase() + display[display.length-1].substr(1) + '</a>, ';
					}
				} else {
					if (parseFloat(property[i]) == parseInt(property[i])) {
						output += property[i];
					} else {
						output += property[i].substr(0,1).toUpperCase() + property[i].substr(1) + ', ';
					}
				}
			} else {
				if (url.exec(property[i])) {
					display = property[i].split('/');
					if (parseFloat(display[display.length-1]) == parseInt(display[display.length-1])) {
						output += '<a href="' + property[i] + '">' + display[display.length-1] + '</a>, ';
					} else {
						output += '<a href="' + property[i] + '">' + display[display.length-1].substr(0,1).toUpperCase() + display[display.length-1].substr(1) + '</a>';
					}
				} else {
					if (parseFloat(property[i]) == parseInt(property[i])) {
						output += property[i];
					} else {
						output += property[i].substr(0,1).toUpperCase() + property[i].substr(1);
					}
				}
			}
		}
		return output;
	} else {
		if (property instanceof Object) {
			output += '<br>';
			for (attribute in property) {
				output+= '<b>'+attribute+': </b>' + org.bibkn.Dataset.display(property[attribute]) + '<br>';
			}
			return output.substring(0,output.length-4);
		} else {
			if (url.exec(property)) {
				display = property.split('/');
				if (display[display.length-1] == '') {
					output += '<a href="' + property + '">' + property + '</a>';
				} else {
					if (parseFloat(display[display.length-1]) == parseInt(display[display.length-1])) {
						output += '<a href="' + property + '">' + display[display.length-1] + '</a>';
					} else {
						output += '<a href="' + property + '">' + display[display.length-1].substr(0,1).toUpperCase() + display[display.length-1].substr(1) + '</a>';
					}
				}
				return output;
			} else {
				if (parseFloat(property) == parseInt(property)) {
					return property;
				} else {
					return property.substr(0,1).toUpperCase() + property.substr(1);
				}
			}
		}
	}
}

function show_data(jsondata) {
	// Convert request(json) to javascript object.
//	var jsondata = eval("("+jsonRequest.responseText+")");
	org.bibkn.Dataset.datasets = jsondata.recordList;
	org.bibkn.Dataset.schema = jsondata.dataset.table_cols;
	org.bibkn.Dataset.reorder(org.bibkn.Dataset.schema[0],'ascending');

}

function getJSON_data(callback, file) {
//	var location = "http://" + window.location.hostname + "/";
//	var service = ""+location+ "bkn/frontpage/" + file;
	$.ajax({
	    url: file,
//	    data: service_params,
	    type: "get",
	    cache: false,
	    dataType: "json",
	    error: function(xobj, status, error){
			    	show_json({'xobj':xobj, 'status':status,'error':error});
			        },
	    success: callback
	}); 
	
}

getJSON_data(show_data,"dod.bib.json");
//org.bibkn.Dataset.load();

