
function show_domains(identifier) {

    var domain_tbody = document.getElementById('Query_Domain_tbody');                      
    domain_tbody.innerHTML = "";
    for (let i = 0; i < query_list.length; i++) {
        var list_info = query_list [i]
        var test = list_info[0]
        if (list_info[0] == identifier ) {
            if (list_info[5] == "SLiM" ) {
                domain_tbody.insertAdjacentHTML('beforeend',`<tr><td><a href="http://elm.eu.org/elms/${list_info[1]}" target="_blank">${list_info[1]}</a></td><td>${list_info[5]}</td><td>${list_info[4]}</td><td>${list_info[2]}</td><td>${list_info[3]}</td></tr>`);
            } else {
                domain_tbody.insertAdjacentHTML('beforeend',`<tr><td><a href="http://pfam.xfam.org/family/${list_info[1]}" target="_blank">${list_info[1]}</a></td><td>${list_info[5]}</td><td>${list_info[4]}</td><td>${list_info[2]}</td><td>${list_info[3]}</td></tr>`);
            }
        }
    }

    var domain_tbody = document.getElementById('Feature_Viewer_Div');
    Feature_Viewer_Div.innerHTML = "";
    create_feature_part ('P0DJ88');

}