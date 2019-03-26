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
        parent.hide();

        $(this).children("input").prop("checked", true);
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

    var $tooltips = $("form .tooltip");
    if (screen.width < 640) {
        $tooltips.attr("data-direction", "bottom");
        $tooltips.parent().click(function (e) {
            e.preventDefault();
        })
    }

    const projectApplications = (function () {
        const $statusWidgets = $(".circle--ajax--applicant-status");

        const init = () => {
            bindUIActions();
        };

        const bindUIActions = () => {
            $statusWidgets.children("span").click(function (e) {
                let widget = $(this).parent();
                hideShowWidget(widget);
            });

            $statusWidgets.children("select").change(function (e) {
                e.preventDefault();

                let widget = $(this).parent();
                let jsonData = updateApplicantWidget(widget);
                const link = `/project/applicant/${jsonData["id"]}/status`;

                ajaxCall(jsonData, link).then(() => {
                        hideShowWidget(widget);
                    }
                ).catch(err => console.log(err));
            });

            $(".circle--ajax--applicant-create, .circle--ajax--applicant-delete").on("click", function (e) {
                e.preventDefault();

                let widget = $(this);

                if (widget.hasClass("circle--ajax--applicant-create")) {
                    createApplicantWidget(widget);
                } else if (widget.hasClass("circle--ajax--applicant-delete")) {
                    deleteApplicantWidget(widget);
                }
            });
        };

        const ajaxCall = function (jsonData, link) {
            const csrftoken = Cookies.get("csrftoken");
            return new Promise((resolve, reject) => {
                $.ajax({
                    url: link,
                    beforeSend: function (xhr) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    },
                    method: "post",
                    data: jsonData,
                    success: function (jsonResponse) {
                        resolve(jsonResponse);
                    },
                    error: function (err) {
                        reject(`Ajax call to ${link} unsuccessful: ${err.statusText}`);
                    }
                });
            });
        };

        const hideShowWidget = (widget) => {
            let $select = widget.children("select");
            let $span = widget.children("span");

            $select.toggle();
            $span.toggle();
        };

        const updateApplicantWidget = (widget) => {
            let $select = widget.children("select");
            let $span = widget.children("span");
            let $chosenValue = $select.find(":selected");

            $span.text($chosenValue.text());
            $select.data("status", $chosenValue.val());

            return $select.data()
        };

        const createApplicantWidget = (widget) => {
            let applicationId = ajaxCall(widget.data(), widget.attr("href"))
                .then(response => {
                        widget.text("You've Applied");
                        widget.removeClass("circle--ajax--applicant-create");
                        widget.addClass("button-inactive");
                        widget.addClass("circle--ajax--applicant-delete");

                        widget.attr("href", `/project/applicant/${response.pk}/delete`);
                    }
                )
                .catch(err => console.log(err));
        };

        const deleteApplicantWidget = (widget) => {
            ajaxCall(widget.data(), widget.attr("href"))
                .then(response => {
                    widget.text("Apply");
                    widget.removeClass("button-inactive");
                    widget.removeClass("circle--ajax--applicant-delete");
                    widget.addClass("circle--ajax--applicant-create");

                    widget.attr("href", "/project/applicant");
                })
                .catch(err => console.log(err));
        };

        return {
            'statusWidgets': $statusWidgets,
            'init': init
        }
    })();
    projectApplications.init();
});
