// A function for calories.html that calculates the calories of a person
function calculate() {
    event.preventDefault();
    let allValid = true;
    let age = Math.floor($("#age").val());

    if (age < 7 || age > 120) {
        allValid = false;
    }

    let height = Number($("#height").val());

    if (height < 120 || height > 251) {
        allValid = false;
    }

    let weight = Number($("#weight").val());

    if (weight < 30 || weight > 420) {
        allValid = false;
    }

    let gender = $("input[name=gender]:checked").val();
    let activityVal = Number($("#activity").val());
    let weightGoal = Number($("#weightGoal").val());

    if (age && height && weight && allValid) {
        let mifflinEquation = Math.floor((10 * weight + 6.25 * height - 5 * age + 5) * activityVal * weightGoal);
        if (gender === "female") {
            mifflinEquation -= 166;
        }
        $("#errors").empty();
        $("#result").empty();
        $("#result").append(`
                <div class="card border-success mb-3">
                    <div class="card-body text-success">
                        <h5 class="card-title">You need to intake ${mifflinEquation} Calories per day to reach your goal.</h5>
                        <form action="/calories" method="post">
                            <input style="display:none;" autocomplete="off" name="caloriesGoal" readonly class="form-control" value ="${mifflinEquation}"/>
                            <button class="btn btn-primary" type="submit">Record goal</button>
                        </form>
                    </div>
                </div>
                `);
    } else {
        $("#errors").empty();
        $("#errors").append(`<p>Please fill in all fields with correct information</p>`);
    }
}

// A function for index.html that hides the elements after the page has loaded
function hideElements(){
        $(window).on('load', function() {
            $("#cover").hide();
            $("#loader").hide();
            $("#quote").hide();
        });
    }

// Validation for recording lifts
function validate() {
    // Getting the id of the error container
    let errorsContainer = document.getElementById("errors");

    // Clearing all previous errors if any
    errorsContainer.innerHTML = "";

    function addError(message) {
        let err = document.createElement("p");
        err.innerText = message;
        errorsContainer.appendChild(err);
        event.preventDefault();
    }

    // Getting inputs from the form
    let sets = document.getElementById("sets").value;
    let reps = document.getElementById("reps").value;
    let weight = document.getElementById("weight").value;

    if (sets === "" || reps === "" || weight === "") {
        addError("Please fill in all the fields");
    } else if (+weight >= 500) {
        addError("Let's be realistic");
    }
}

function firstTimeValidate() {
    // Getting the id of the error container
    let errorsContainer = document.getElementById("errors");

    // Clearing all previous errors if any
    errorsContainer.innerHTML = "";

    // Getting inputs from the form
    let currentORM = document.getElementById("currentORM").value;
    let goal = document.getElementById("goal").value;


    // Appends children to the HTML
    function addError(message) {
        let err = document.createElement("p");
        err.innerText = message;
        errorsContainer.appendChild(err);
        event.preventDefault();
    }

    if (currentORM === "" || goal === "") {
        addError("Please fill in all the fields");
    } else if (+currentORM >= +goal) {
        addError("Don't be weak");
    } else if (+goal >= 500) {
        addError("Let's be realistic");
    }
}

function pullupsValidate() {
    // Getting the id of the error container
    let errorsContainer = document.getElementById("errors");

    // Clearing all previous errors if any
    errorsContainer.innerHTML = "";

    // Getting inputs from the form
    let sets = document.getElementById("sets").value;
    let reps = document.getElementById("reps").value;

    // Appends children to the HTML
    function addError(message) {
        let err = document.createElement("p");
        err.innerText = message;
        errorsContainer.appendChild(err);
        event.preventDefault();
    }

    if (sets === "" || reps === "") {
        addError("Please fill in all the fields");
    } else if (+reps >= 300) {
        addError("Let's be realistic");
    }
}

function loginValidate() {
    // Getting the id of the error container
    let errorsContainer = document.getElementById("errors");

    // Clearing all previous errors if any
    errorsContainer.innerHTML = "";

    // Getting inputs from the form
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    // Appends children to the HTML
    function addError(message) {
        let err = document.createElement("p");
        err.innerText = message;
        errorsContainer.appendChild(err);
        event.preventDefault();
    }

    if (username === "") {
        addError("Missing username");
    }

    if (password === "") {
        addError("Missing password");
    }
}

function newPassValidate() {
    // Getting the id of the error container
    let errorsContainer = document.getElementById("errors");

    // Clearing all previous errors if any
    errorsContainer.innerHTML = "";

    // Getting inputs from the form
    let password = document.getElementById("password").value;
    let newpassword = document.getElementById("newpassword").value;
    let passConfirmation = document.getElementById("confirmation").value;

    // A regex to test whether a string contains a number
    let hasNumber = /\d/;

    // Appends children to the HTML
    function addError(message) {
        let err = document.createElement("p");
        err.innerText = message;
        errorsContainer.appendChild(err);
        event.preventDefault();
    }

    if (password === "" || newpassword === "" || passConfirmation === "") {
        addError("Please fill in all the fields");
    } else if (newpassword.length < 6) {
        addError("Password must be at least 6 characters");
    } else if (!hasNumber.test(newpassword)) {
        addError("Password should include at least one number");
    } else if (newpassword !== passConfirmation) {
        addError("Passwords should match");
    } else if (newpassword === password) {
        addError("New password should be different")
    }
}

function registerValidate() {
    // Getting the id of the error container
    let errorsContainer = document.getElementById("errors");

    // Clearing all previous errors if any
    errorsContainer.innerHTML = "";

    // A regex to test whether a string contains a number
    let hasNumber = /\d/;

    // Getting inputs from the form
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    let passConfirmation = document.getElementById("confirmation").value;

    // Appends children to the HTML
    function addError(message) {
        let err = document.createElement("p");
        err.innerText = message;
        errorsContainer.appendChild(err);
        event.preventDefault();
    }

    if (username === "") {
        addError("Username cannot be empty");
    } else if (username.length < 4 || username.length > 24) {
        addError("Username must be between 4 and 24 characters");
    }

    if (password === "") {
        addError("Password cannot be empty");
    } else if (password.length < 6) {
        addError("Password must be at least 6 characters");
    } else if (!hasNumber.test(password)) {
        addError("Password should include at least one number");
    } else if (password !== passConfirmation) {
        addError("Passwords should match");
    }
}

function postValidate() {
    // Getting the id of the error container
    let errorsContainer = document.getElementById("errors");

    // Clearing all previous errors if any
    errorsContainer.innerHTML = "";

    // Getting inputs from the form
    let post = document.getElementById("post").value;

    // Appends children to the HTML
    function addError(message) {
        let err = document.createElement("p");
        err.innerText = message;
        err.style.color = "red";
        errorsContainer.appendChild(err);
        event.preventDefault();
    }

    if (post === "") {
        addError("The field is empty");
    } else if (post.length >= 250) {
        addError("The post must be below 250 characters");
    }
}

// Checks for calories and other nutrients in foods
function check() {
    let userInput = $("#check").val();
    load();
    async function load() {
        try {
            let info = await $.ajax({
                url: 'https://api.edamam.com/api/food-database/parser?nutrition-type=logging&ingr=' + encodeURI(userInput) + '&app_id=1195a140&app_key=cc3cf2d2de00d424ff15531b7691db30',
                method: "GET"
            });
            let grams = Number($("#grams").val()) / 100;
            if (grams <= 0) {
                grams = 0;
            }
            if (info.parsed.length !== 0) {
                $("#table").show();
                $("#errors").empty();
                let foodContainer = [];
                for (let ings of info.parsed) {
                    let calories = isNanCheck(Math.floor(ings.food.nutrients.ENERC_KCAL * grams));
                    let proteins = isNanCheck(Math.floor(ings.food.nutrients.PROCNT * grams));
                    let fat = isNanCheck(Math.floor(ings.food.nutrients.FAT * grams));
                    let carbs = isNanCheck(Math.floor(ings.food.nutrients.CHOCDF * grams));
                    $("#results").append(`
                            <tr>
                                <td>${ings.food.label}</td>
                                <td>${calories}</td>
                                <td>${proteins}</td>
                                <td>${fat}</td>
                                <td>${carbs}</td>
                            </tr>`);
                    $("#calSum").text(Number($("#calSum").text()) + calories);
                    $("#proteinSum").text(Number($("#proteinSum").text()) + proteins);
                    $("#fatSum").text(Number($("#fatSum").text()) + fat);
                    $("#carbSum").text(Number($("#carbSum").text()) + carbs);
                    $("#button").show();
                    $("#calorieInput").val(Number($("#calSum").text()));
                    foodContainer.push(ings.food.label);
                }
                console.log(foodContainer);
                $("#food").val(foodContainer); //.join(", "));
            } else {
                $("#errors").empty();
                $("#errors").append(`<p>Ooops, nothing in our database matches what you are searching for. Please try again</p>`);
            }
        } catch (err) {
            $("#errors").append(`<p>Something went wrong. Please try again</p>`);

        }
    }

    function isNanCheck(nutrient) {
        if (isNaN(nutrient)) {
            return 0;
        }
        return nutrient;
    }
}