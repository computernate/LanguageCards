import Kuroshiro from "kuroshiro";
// Initialize kuroshiro with an instance of analyzer (You could check the [apidoc](#initanalyzer) for more information):
// For this example, you should npm install and import the kuromoji analyzer first
import KuromojiAnalyzer from "kuroshiro-analyzer-kuromoji";
// Instantiate
const kuroshiro = new Kuroshiro();
// Initialize
// Here uses async/await, you could also use Promise
await kuroshiro.init(new KuromojiAnalyzer());

const cols = 5;
const rows = 9;

async function run(){
	var input = document.getElementById("input").value;
	input=input.replace(/[\n\r]/g, ",");
	data = input.split(/,(?=(?:(?:[^"]*"){2})*[^"]*$)/);
	console.log(data)
	pages = Math.ceil(data.length / 6 / (cols*rows))
	var final_data = ""

	var kuroshiro = new Kuroshiro();

	for(var a=0;a<pages;a++){
		for_counter = (a==pages-1)?data.length/6%(cols*rows):cols*rows;
		final_data+="<table>"
		for(var b=0;b<for_counter;b++){
			if(b%cols==0) final_data+="<tr>"
			else if(b%cols==cols) final_data+="</tr>"
			var curr_data = data[(b+(a*cols*rows))*6+5]
			if(curr_data==undefined)break;
			curr_data = curr_data.replace(/[^\x00-\x7F]/g,"")
			final_data+="<td>"+curr_data+"</td>";
		}
		final_data+="</table><table>"
		for(var b=0;b<rows;b++){
			final_data+="<tr>"
			for(var c=(cols-1);c>=0;c--){
				try{
					kanji = data[(((b*cols)+c+(a*cols*rows)))*6];
					var hira = kuroshiro.convert(kanji, {to:"hiragana"});
					final_data+="<td><p>"+hira+"</p><p>"+data[(((b*cols)+c+(a*cols*rows)))*6+1]+"</p></td>";
				}
				catch{
					final_data+="</tr>"
					final_data+="</table>"
					document.getElementById("output").innerHTML=final_data;
					return;
				}
			}
			final_data+="</tr>"
		}
		final_data+="</table>"
	}
	document.getElementById("output").innerHTML=final_data;
}