$(document).ready(function () {
    $('#Interaction_Table').DataTable({
        "pagingType": "numbers",
        "searching": true,
        "lengthChange": true,
    });

    $('#Query_Protein_Table').DataTable({
        "pagingType": "numbers",
        "searching": false,
        "lengthChange": true,
    });

    $('#Query_Protein_Inferred_Full_Table').DataTable({
        "pagingType": "numbers",
        "searching": true,
        "lengthChange": true,
    });

    $('#Query_Protein_Inferred_Filtered_Table').DataTable({
        "pagingType": "numbers",
        "searching": true,
        "lengthChange": true,
    });

    $('#Query_Slims_Domains_Table').DataTable({
        "pagingType": "numbers",
        "searching": true,
        "lengthChange":true,
    });
    $('#Enrichment_Table').DataTable({
        "pagingType": "numbers",
        "searching": true,
        "lengthChange": true,
    });
    $('.dataTables_length').addClass('bs-select');
});