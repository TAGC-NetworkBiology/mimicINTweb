update_network();

function create_network(){
        var query_layout = document.getElementById("layout");
        var init_layout = query_layout.options[query_layout.selectedIndex].value;
        var cy = (window.cy = cytoscape({
            container: document.getElementById('cy'),
            style: cytoscape.stylesheet()
                .selector('node[type="target"]')
                .css({
                    shape: 'roundrectangle',
                    'background-color': '#85888d',
                    'width': '60px',
                    'height': '20px',
                    'content': 'data(id)',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'font-size': '8%',
                    'color': "#eeeeee",
                })
                .selector('node[type="query"]')
                .css({
                    shape: 'ellipse',
                    'background-color': "#e27400",
                    'width': '60px',
                    'height': '20px',
                    'content': 'data(id)',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'font-size': '8%',
                    'color': "#eeeeee",
                })

                .selector('edge[type="1"]')
                .css({
                    'width': 2,
                    'opacity': 0.8,
                    'line-color': '#1A5276',
                    "curve-style": "bezier", 
                })
                .selector('edge[type="2"]')
                .css({
                    'width': 2,
                    'opacity': 0.8,
                    'line-color': '#b6d7ea',
                    "curve-style": "bezier",
                })
                .selector('edge[type="3"]')
                .css({
                    'width': 2,
                    'opacity': 0.8,
                    'line-color': '#483D8B',
                })

                .selector(':selected')
                .css({
                    'background-color': '#f1c40f',
                    'line-color': '#f1c40f',
                    'target-arrow-color': '#f1c40f',
                    'source-arrow-color': '#f1c40f',
                    'opacity': 1
                })
                .selector('.faded')
                .css({
                    'opacity': 1,
                    'text-opacity': 1
                }),

            elements: data_network,

            layout: {
                name: init_layout, //cose, random, grid, circle, concentric, breadthfirst
                padding: 10
            },

        }));
        const nodesWithoutEdges = cy.nodes().filter(node => node.connectedEdges(":visible").size() === 0)
        cy.remove (nodesWithoutEdges);
}


function update_layout(){
    var query_layout = document.getElementById("layout");
    var new_layout = query_layout.options[query_layout.selectedIndex].value;
    cy.ready(function() {
        var layout = cy.layout({ name: new_layout, padding: 10 }); 
        layout.run();
    });   
}


function update_network(){
    create_network();
    var target_degree = document.getElementById("target_degree");
    var min_target_degree = target_degree.options[target_degree.selectedIndex].value;
    cy.remove('node[target_degree < ' + min_target_degree + ']');
    
    var query_degree = document.getElementById("query_degree");
    var min_query_degree = query_degree.options[query_degree.selectedIndex].value;
    cy.remove('node[query_degree < ' + min_query_degree + ']');

    var interaction = document.getElementById("edges");
    var interaction_type = interaction.options[interaction.selectedIndex].value;
    if (interaction_type == 0) {
        cy.remove('edge[type = "3"]');
    } else {
        cy.remove('edge[type != "' + interaction_type + '"]');
    }
    
    const nodesWithoutEdges = cy.nodes().filter(node => node.connectedEdges(":visible").size() === 0);
    cy.remove (nodesWithoutEdges);
    verify_number_of_nodes();
    update_layout();
}


function verify_number_of_nodes()
{
    var number_of_nodes = cy.nodes().size();
    if (cy.nodes().size() > 50) {
        const all_nodes = cy.nodes();
        cy.remove (all_nodes);
        var cytoscape_message = document.getElementById('cytoscape_message');
        cytoscape_message.innerHTML = "To many nodes, please use filters.";
    } else {
        var cytoscape_message = document.getElementById('cytoscape_message');
        cytoscape_message.innerHTML = " ";       
    }
}
