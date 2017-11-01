function getValue(){
    $(document).ready(function(){
        var container = []
        $("select").imagepicker({
            selected: function(option){
                var value = this.val();
                container.push(value);
                alert(container);
            }
        });
    });
}

function placeImages(json_lst, min){
    var oder = {
        images : ["odor_almond.jpeg", "odor_anise.jpeg", "odor_creosote.jpg", "odor_fishy.jpg", "odor_foul.jpg", "odor_musty.jpeg", "odor_none.jpeg", "odor_pungent.jpg", "odor_spicy .jpg"],
        values : ["a", "l", "c", "y", "f", "m", "n", "p", "s"],
        text : ["Almond", "Anise", "Creosote", "Fishy", "Foul", "Musty", "None", "Pungent", "Spicy"]
    };

    var gill_size = {
        images : ["broad_gillsize.jpeg", "narrow_gillsize.jpeg"],
        values : ["b", "n"],
        text : ["Broad gill-size", "Narrow gill-size"]
    };

    var spore_print_color = {
        images : ["spc_black.jpg","spc_brown.jpg", "spc_buff.jpg", "spc_chocolate.jpeg", "spc_green.png", "spc_orange.jpeg", "spc_purple.jpeg", "spc_white.jpeg", "spc_yellow.jpg"],
        values : ["k", "n", "b", "h", "r", "o", "u", "w", "y"],
        text : ["Black", "Brown", "Buff", "Chocolate", "Green", "Orange", "Purple", "White", "Yellow"]
    };

    var habitat = {
        images : ["hab_grasses.jpeg", "hab_leaves.jpeg", "hab_meadow.jpg", "hab_path.jpg", "hab_urban.jpg", "hab_waste.jpeg", "hab_woods.jpg"],
        values : ["g", "l", "m", "p", "u", "w", "d"],
        text : ["Grasses", "Leaves", "Meadows", "Paths", "Urban", "Waste", "Woods"]
    };


    var max = json_lst.length - 1, select = document.getElementByClass('picker')

    if(min <= max){

        for (i = 0; i <= eval(json_lst)[min].images.length - 1; i++){
            var opt = document.createElement("option");
            opt.setAttribute('value') = json_lst[min].values[i]
            opt.setAttribute('data-img-src') = '~/DS_practice/mushroom_project/mushroom_app/static/feature_imgs' + json_lst[min].images[i]
            opt.setAttribute('innerHTML') = json_lst[min].text[i]
        };
        min = min + 1
        return min
    }
    else {
        alert("You have made a selection for each parameter. Please hit the submit button. ");
    }
}

function removeOptions(select){
    $(document).ready(function(){
    $("select").imagepicker({
        selected:function(option){
            alert(select.options.length)
        var i;
        for (i = select.options.length - 1; i >= 0; i-- )
                {
                    select.remove(i);
                }
            }

        });
    });
}


var feature_lst = new Array("oder", "gill_size", "spore_print_color", "habitat");
