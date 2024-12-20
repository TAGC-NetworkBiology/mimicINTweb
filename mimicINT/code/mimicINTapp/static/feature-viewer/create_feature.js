function create_feature_part (identifier){
    
    var protein_features = data_features[identifier];

    //Create a new Feature Viewer and add some rendering options
    var ft = new FeatureViewer(protein_features["sequence"],"#Feature_Viewer_Div", {
        showAxis: true,
        showSequence: true,
        brushActive: true,
        toolbar:true,
        bubbleHelp:true,
        zoomMax:10
    });

/*
    ft.addFeature({
        data: [{x:20,y:32},{x:46,y:100},{x:123,y:167}],
        name: "Trans. Region",
        color: "#005572",
        type: "rect",
        filter: "type1"
    });
    ft.addFeature({
        data: [{x:52,y:52},{x:92,y:92}],
        name: "Clivage Site",
        className: "test2",
        color: "#006588",
        type: "rect",
        filter: "type2"
    });
*/

    ft.addFeature({
        data: protein_features["domains"],
        name: "Domains",
        color: "#F4D4AD",
        type: "rect",
        filter: "type2"
    });

    ft.addFeature({
        data: protein_features["motifs"],
        name: "Motifs",
        color: "#D4B49D",
        type: "rect",
        filter: "type2"
    });


    ft.addFeature({
        data: protein_features["IUPRED"],
        name: "IUPRED",
        color: "#008B8D",
        type: "line",
        filter: "type2",
        height: "5"
    });
}