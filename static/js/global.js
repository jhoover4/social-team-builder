$(document).ready(function () {
    const $circleCloneList = $(".circle--clone--list");

    $('textarea').autogrow({onInitialize: true});

    const updateDjangoCounter = (num) => {
        const $totalFormsInput = $("#id_projectposition_set-TOTAL_FORMS");
        const newFormNum = parseInt($totalFormsInput.val()) + num;

        $totalFormsInput.val(+newFormNum);
        return newFormNum;
    };

    const updateFormSetAttr = (form, count) => {
        // form.find("input, textarea, select").attr("id", `projectposition_set-${count - 1}-name`);
        form.find("input, textarea, select").attr("id", function (i, name) {
            return name.replace(/\d+/, count - 1);
        });
        form.find("input, textarea, select").attr("name", function (i, name) {
            return name.replace(/\d+/, count - 1);
        });
    };

    //Cloner for infinite input lists
    $circleCloneList.on("click", ".circle--clone--add", function () {
        var parent = $(this).parent("li");
        var copy = parent.clone();
        parent.after(copy);
        copy.find("input, textarea, select").val("");
        copy.find("*:first-child").focus();

        let formCount = updateDjangoCounter(1);
        updateFormSetAttr(copy, formCount);
    });

    $circleCloneList.on("click", "li:not(:only-child) .circle--clone--remove", function () {
        var parent = $(this).parent("li");
        parent.remove();

        updateDjangoCounter(-1);
    });

    // Adds class to selected item
    $(".circle--pill--list a").click(function () {
        $(".circle--pill--list a").removeClass("selected");
        $(this).addClass("selected");
    });

    // Adds class to parent div of select menu
    $(".circle--select select").focus(function () {
        $(this).parent().addClass("focus");
    }).blur(function () {
        $(this).parent().removeClass("focus");
    });

    // Clickable table row
    $(".clickable-row").click(function () {
        var link = $(this).data("href");
        var target = $(this).data("target");

        if ($(this).attr("data-target")) {
            window.open(link, target);
        } else {
            window.open(link, "_self");
        }
    });

    // Custom File Inputs
    var input = $(".circle--input--file");
    var text = input.data("text");
    var state = input.data("state");
    input.wrap(function () {
        return "<a class='button " + state + "'>" + text + "</div>";
    });

//     $.ajax({
//     url:  '/rooms/list',
//     type:  'post',
//     dataType:  'json',
//     success: function  (data) {
//         let rows =  '';
//         data.rooms.forEach(room => {
//         rows += `
//         <tr>
//             <td>${room.room_number}</td>
//             <td>${room.name}</td>
//             <td>${room.nobeds}</td>
//             <td>${room.room_type}</td>
//             <td>
//                 <button class="btn deleteBtn" data-id="${room.id}">Delete</button>
//                 <button class="btn updateBtn" data-id="${room.id}">Update</button>
//             </td>
//         </tr>`;
//     });
//     $('[#myTable](https://paper.dropbox.com/?q=%23myTable) > tbody').append(rows);
//     $('.deleteBtn').each((i, elm) => {
//         $(elm).on("click",  (e) => {
//             deleteRoom($(elm))
//         })
//     })
//     }
// });
});
