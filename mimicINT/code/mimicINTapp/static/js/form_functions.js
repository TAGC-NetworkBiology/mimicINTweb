


function validateForm() {
    var protein_set = document.forms["myForm"]["id_query_sequencies"].value;
    var lines = protein_set.split('\n');
    lines = lines.filter(Boolean);
    var number_of_protein = 0;
    for (let i = 0; i < lines.length; i++) {
        if (lines[i][0] == '>') {
            if (/^[a-zA-Z]+$/.test(lines[i]) == false) {
                number_of_protein +=1;                   
            } else {
                 alert("No valid header format!");
                return false;                   
            }
        } else {
            if (/^[A-Z]+$/.test(lines[i]) == false) {
                alert("No valid protein format!");
                return false;
            }
        }
    }
    /*
    var number_of_protein = (protein_set.match(new RegExp("\n", "g")) || []).length;
    */
    if (number_of_protein > 50) {
        alert("To mutch proteins!");
        return false;
    } else if (number_of_protein == 0) {
        alert("No proteins!");
        return false;          
    }
}


function file_to_textarea() {
    var file = document.getElementById("id_query_fasta_file").files[0];
    var reader = new FileReader();
    reader.onload = function (e) {
        var textArea = document.getElementById("id_query_sequencies");
        textArea.value = e.target.result;
    };
    reader.readAsText(file);
}


function example_to_textarea() {
    document.getElementById("id_query_sequencies").value = fasta_example;
}

function reset_options(){
    var dropDown = document.getElementById("iumethod");
    dropDown.selectedIndex = 0;
    
    var field= document.getElementById('conserved_motifs');
    field.value= field.defaultValue;
    var field= document.getElementById('iucut');
    field.value= field.defaultValue;
    var field= document.getElementById('minregion');
    field.value= field.defaultValue;
    var field= document.getElementById('domain_score_threshold');
    field.value= field.defaultValue;
}