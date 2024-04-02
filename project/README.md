# PROJECT TITLE:  PET EXPENSE TRACKER

#### Video Demo: < https://youtu.be/VYSSv2aDCN4>

#### Description

##### Introduction:
*Pet Expense Tracker* is simple web application created using Python, Javascript, and SQL. I am pet lover, we love pets, but sometimes, the expense for them becomes a big cost in our budget, so I created this wed application to keep track the expense for the pets. The web application has total 6 tabs with different function at each tab:
- **Pet Type tab**: to let users adding *pet type*. By default, the registered user has **cat** and **dog**.
- **Add Pet tab**: Lets users add their *pets*.
- **Service Type tab**: Lets users add *pet service type* if not available in the system. By default, the registered user has 4 pet service types: **Food**, **Treats**, **Pet supplies**, **Pet services**.
- **Category tab**: Lets users add *pet category* if not available in the system. Categories are associated with pet service type. The above default pet service types has 3 or 4 categories associated with it by default.
    Example: Food has 4 categories: **Dry food**, **Canned food**, **Semi-moist food**, **Fresh pet food** (*details will mention at **Details of Project** section*)
- **Add Expense tab**: Lets users add expenses which they spent for their pets.
- **Expense History tab**: Displays a list of all the expenses.


##### Technologies:
- Python3
- Flask3
- SQLite3
- JavaScript


##### **Installation**:
For me, I connected my local VS Code with my CODESPACES
- Install VSCode link here <https://code.visualstudio.com/>, down load the stable build in your local computer.
- Go to <https://code.cs50.io/>, click **open in VS Code Desktop** to connect/access CODESPACE, and just coding this project.

- You can install and configure environment complete locally on your computer by install windows sub-system for Linux link here <https://ubuntu.com/wsl>, then go to VS Code install extension: Remote -WSL. Open folder in WSL, then enter in terminal windown:
    ```
      sudo apt-get update (this app to let us install any package)
    ```
    Next, install Python3, Flask, CS50, and SQLite3
    ```
    sudo apt-get install python3
    sudo apt-get install python3-pip
    pip3 install flask
    pip3 install flask-session
    pip3 install cs50
    sudo apt-get install sqlite3
    ```


##### Details of Project:
**Pet Expense Tracker** Lets users keep track their expenses for their pets, including date, type, category, pet name, and the amount ($). It has total of **12 HTML templates** served for 6 tabs, each tab has its own function.  Users **must register** to use this application.

- **Register function**: Lets users register in the web application.
  **register.html** template creates the UI as following screenshot:
![register](./static/image/markdown_screenshots/Register.jpg)

**fields data validation** as folowing screenshot:
![register_FieldsValidations](./static/image/markdown_screenshots/Register_fieldsValidation.jpg)
Code is here:
```
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmPassword = request.form.get("passwordConfirmation")
        # check not input username
        if not username:
            return apology("must provide username", 400)
        # check max length of username
        if len(username) > 50:
            return apology("max length of username is 50 characters")
        # check not input password
        if not password:
            return apology("must provide password", 400)
        # check not input confirm password
        if not confirmPassword:
            return apology("must provide password confirmation", 400)
        # check password and confirm password does not match
        if confirmPassword != password:
            return apology("password and confirm password do not match", 400)
        # check username already existed in DB
        existingUsers = db.execute("SELECT * FROM users WHERE UPPER(username) = ?", username.upper())
        if len(existingUsers) > 0:
            return apology(
                "username already existed, please enter another username", 400
            )
```
After the user successfully registers, the user is inserted in DB as following screenshot:
![users_table](./static/image/markdown_screenshots/users_table.jpg)

**Source code app.py**: please access the **GitHub** link at the end of the README file.



- **Login function**: Lets the user sign in the web application
**Login.html** template creates the Login UI as following screenshot:
![login](./static/image/markdown_screenshots/Login.jpg)
**fields data validation** code here:
```
 if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)
```
**Source code app.py**: Please access the **GitHub** link at the end of README file.


After a successful login, you will land on the **Pet Portfolio** page with 6 navigated tabs: Pet Type, Add Pet, Service Type, Category, Add Expense, Expense History.

- **1. Pet Type tab**:  Lets user input the *pet type* if it doesn't exist in the system. **petType.html** template creates *Pet Type* UI as following screenshot:
![addPetType](./static/image/markdown_screenshots/AddPetType.jpg)
**Available pet types in the system** dropdown (for **view only**), to let user know these pet types already existed in the system. Registered user has two pet types **by default**: **Cat** and **Dog**. If user wants to add the different pet type, just input it in the **Pet Type** input field, then click **ADD** button as following screenshot:
![AddPetType](./static/image/markdown_screenshots/AddPetType_Squirrel.jpg)

After successfully adding a pet type, the system will display **success.html** with some guidance as following screenshot: (second guidance)
![SuccessAdded](./static/image/markdown_screenshots/SuccessAdded.jpg)

**Pet type fields data validation** as screenshot:
![petType_fieldsValidation](./static/image/markdown_screenshots/petType_fieldsDataValidation.jpg)
*Code here*
```
@app.route("/addPetType", methods=["GET", "POST"])
@login_required
def addPetType():
    """Add Pet Type"""
    defaultPetType = db.execute("SELECT user_id, type FROM pet_types WHERE user_id = ?", session["user_id"])
    # Add pet type
    if request.method == "POST":
        petType = request.form.get("petType")
        # check pet type is required
        if not petType:
            return apology("Pet Type is required field")
        # check pet type already existed in DB
        existedPetType = db.execute("SELECT * FROM pet_types WHERE user_id =? and UPPER(type) =?", session["user_id"], petType.upper())
        if len(existedPetType) > 0:
            return apology("Pet type already existed")
```
**Source code app.py**: Please access the link at the end of README file.


- **2. Add Pet tab**: Lets the user add their pets.
**addPet.html** template creates the UI of this page as following screenshot:
![addPet](./static/image/markdown_screenshots/addPet.jpg)

**Add Pet fields data validation** as following screenshot:
![AddPet_fieldValidation](./static/image/markdown_screenshots/AddPet_fieldsValidation.jpg)
*Code here*
```
@app.route("/addPet", methods=["GET", "POST"])
@login_required
def addPet():
    availablePetTypesInDB = db.execute("SELECT * FROM pet_types WHERE user_id = ?", session["user_id"], )
    """Add pet."""
    if request.method == "POST":
        petType = request.form.get("petType")
        petName = request.form.get("petName")
        dateOfBirth = request.form.get("dob")
        sex = request.form.get("sex")
        note = request.form.get("addNote")
        if not petType:
            return apology("Pet Type is required")
        if not petName:
            return apology("Pet Name is required")
        if not dateOfBirth:
            return apology("Date of Birth is required")
        petTypeId = db.execute("SELECT id FROM pet_types WHERE user_id = ? and type = ?", session["user_id"], petType)
        petType_Id = petTypeId[0]["id"]
        existedNameInDB = db.execute("SELECT name FROM pets WHERE user_id = ? and UPPER(name) = ?", session["user_id"], petName.upper())
        if len(existedNameInDB) > 0:
            return apology("Pet Name already existed")
```

Input data in all fields (at least required fields), then click ADD button as following screenshot:
![addPet](./static/image/markdown_screenshots/addPet_inputAllFields.jpg)
After successfully adding a Pet, the **success.html** template will display with guidances (*the first guidance*). You already saw the UI of *success.html* template above. Here is the *HTML code*
```{% block main %}
    <form class="sendSuccess" action="/success" method = "post">
        <p class="info"><strong>ADDED SUCCESSFULLY</strong></p>

        <p>Your added pet will be displayed at <strong>Pet Portfolio page</strong></p>

        <p>Added pet type, service type, category type will be appeared at <strong>drop down after adding</strong></p>

        <p>Your added expense will be displayed at Expense History. Please click on <a href="/expenseHistory">this link</a> or navigate tab <strong>Expense History</strong></p>

        <button class="btn btn-primary" type="submit">Back To Pet Portfolio</button>
    </form>
{% endblock %}

```
Following the *first guidance*, and click on **Back To Pet Portfolio** button, system will bring you to **Pet Portfolio** page, here you will see the pet you just added.


- **3. Pet Portfolio page**: Displays all your pets.
**Index.html** template creates the UI for this page as following screenshot:
![petPortfolio](./static/image/markdown_screenshots/petPortfolio.jpg)

*source code app.py* link is the end of the README.md file.


- **4. Service Type tab**: Let the user add the pet service type if it does not exist in the system.
**serviceType.html** template creates the UI for this page as following screenshot:
![PetServiceType](./static/image/markdown_screenshots/petServiceType.jpg)
**Available pet service types in the system** drop-down (**view only**) to let user know the **existed** service types in the system. The registered user has **4 pet service types** by default: Food, Treats, Pet supplies, Pet services. If user wants another different service type, so user can add it here by input data in the *Pet Service Type* input field, then click ADD button. *Example* as following screenshot:
![addPetServiceType](./static/image/markdown_screenshots/addPetServiceType.jpg)

After successfully adding a pet service type, when go back to this tab, you will see it at the dropdown as following screenshot:
![petServiceType_addedSuccess](./static/image/markdown_screenshots/petServiceType_addedSuccess.jpg)

**fields data validation** code here:
```
@app.route("/addServiceType", methods=["GET", "POST"])
@login_required
def addServiceType():
    """Add Pet Service Type"""
    defaultServiceTypes = db.execute("SELECT type FROM service_types WHERE user_id = ?", session["user_id"])
    if request.method == "POST":
        serviceType_forPet = request.form.get("petServiceType")
        # check pet service type is required
        if not serviceType_forPet:
            return apology("Pet Service Type is required field")
        # check pet service type already existed
        existedPetServiceTypeInDB = db.execute("SELECT type FROM service_types WHERE user_id = ? and UPPER(type) = ?", session["user_id"], serviceType_forPet.upper())
        if len(existedPetServiceTypeInDB) > 0:
            return apology("Service Type already existed")
```
**source code app.py** link is the end of this README.md file


- **5. Category tab**: Lets the user add the pet category if it doesn't exist in the system.
**category.html** template is created for UI of this page as following screenshot:
![categories](./static/image/markdown_screenshots/Categories.jpg)

**Pet categories are associated with Pet service Type**. User **must select the Pet service type**, then system will display the categories associated with that service type. **By default**, system has some default categories associated with 4 default service types:
**Food** has default categories: Dry food, Canned food, Semi-moist food, Fresh pet food.
**Treats** has default categories: Dog treats, Cat treats, Dental treats, Bird treats.
**Pet supplies** has default categories: Beds, Feeder, Cleaning supplies.
**Pet services** has default categories: Veterinary care, Grooming, Training classes, Petshotel boarding, Doggie day camp.
**JavaScript** wrote for the function *Pet categories will be displayed associated with the selected Pet service type* here
```
function popCategories(categories) {
    var serviceTypeDropdown = document.getElementById("availableServiceType");
    var categoryDropdown = document.getElementById("availableCategory");
    // get serviceTypeId associated with selected service type
    var selectedServiceTypeId = serviceTypeDropdown.value;
    // get categories associated with the specific service type
    var selectedCategories = categories.filter(function(data) {
        return data.service_type_id == selectedServiceTypeId;
    });

    //remove category values in dropdown when user selected another service type
    var i, L = categoryDropdown.options.length - 1;
        for(i = L; i >= 0; i--) {
            categoryDropdown.remove(i);
    }

    //display category in the categorydropdown
    var option = document.createElement("option");
        option.value = "NULL";
        option.text = ""
        categoryDropdown.add(option);
    for (var i = 0; i < selectedCategories.length; i++) {
        var option = document.createElement("option");
        option.value = selectedCategories[i].id;
        option.text = selectedCategories[i].category;
        categoryDropdown.add(option);
    }
}
```

**Available pet categories in the system** drop-downs to let user know the **existed** pet service type and categories in the system. **Pet category drop-down for view only**.

If user wants to add *another different pet category*, **user must select Pet Service Type** at drop-down, then input data in the **Pet Category** input field, then click ADD button as following screenshot:
![Category_add](./static/image/markdown_screenshots/Category_add.jpg)

**Categories fields data validation** screenshot:
![categories_fieldsValidation](./static/image/markdown_screenshots/Category_fieldsDataValidation.jpg)
**fields validation** code here:
```
@app.route("/addCategory", methods=["GET", "POST"])
@login_required
def addCategory():
    """Add Pet Category"""
    serviceTypes = db.execute("SELECT id, type FROM service_types WHERE user_id = ?", session["user_id"])
    categories = db.execute("SELECT id, service_type_id, category FROM categories WHERE user_id = ?", session["user_id"])
    if request.method == "POST":
        selectedPetServicetype = request.form.get("serviceType")
        petCategory = request.form.get("petCategory")
        # check must select pet service type before adding pet category
        if not selectedPetServicetype:
            return apology("Pet service type is required before adding pet category")
        # check pet category is required
        if not petCategory:
            return apology("pet Category input field is required")

        existedPetCategoryInDB = db.execute("SELECT user_id, service_type_id, category FROM categories WHERE user_id=? and service_type_id=? and UPPER(category) =?", session["user_id"], selectedPetServicetype, petCategory.upper())
        if len(existedPetCategoryInDB) > 0:
            return apology('Pet category already existed')

```
After successfully adding a Category, go back to this tab, you will see it at **Pet Category** drop-down.
**source code app.py** link is at the end of the README.md


- **6. Add Expense tab**: Lets the user add the expenses for their pets.
**addExpense.html** template creates for the UI of this page as following screenshot:
![addExpense](./static/image/markdown_screenshots/addExpense.jpg)
As mentioned above, **Pet Categories** are associated with **Pet Service Types**, so you **must select Pet Service Type**, then system will display **Pet categories** associated with the selected service type. If you don't see *Pet Service Type* and *Pet Categories* which you want. Please visit *Service Type* tab and *Category* tab to add them, then come back this page.

All fields are required (except *Pet categories* and *Pet* are optional)
**Fields data validation** as following screenshot:
![addExpense_fieldsValidation](./static/image/markdown_screenshots/addExpense_fieldsdataValidation.jpg)
![addExpense_fieldsValidationTwo](./static/image/markdown_screenshots/addExpense_fieldsValidationTwo.jpg)
**Fields validation** code here:
```
    if request.method == "POST":
        petServiceType = request.form.get("serviceType")
        petCategory = request.form.get("category")
        petId = request.form.get("petName")
        description = request.form.get("description")
        amount = request.form.get("amount")
        date = request.form.get("date")
        today = datetime.now().date()
        # check pet service type is required
        if not petServiceType:
            return apology("Pet service type is required")
        # check description is required
        if not description:
            return apology("description is required")
        # check amount is required
        if not amount:
            return apology("amount is required")
        # check amount is positive number
        if not is_number(amount) or float(amount) < 0:
            return apology("amount must be positive number")
        # check date is required
        if not date:
            return apology("date is required")
        # check input date not in the future
        userDateInput = datetime.strptime(date, '%Y-%m-%d').date()
        if userDateInput > today:
            return apology("date should not be future date")
```

To add an expense, input data into all fields (at least required fields), the click on ADD button as following screenshot:
![addExpense_Details](./static/image/markdown_screenshots/addExpense_Details.jpg)
After successfully adding an expense, the **sucess.html** template will display with the guidance (3rd guidance) to go *Expense History* page to see the expense which you just added.
**source code app.py** link is the end to this README.md file.



- **7. Expense History tab**: Lets the user see all the expenses for their pets in details and TOTAL spending.
**expenseHistory.html** creates for the UI of this page as following screenshot:
![expenseHistory](./static/image/markdown_screenshots/expenseHistory.jpg)

**Future enhancements** for this page could include more  report options based on date, year, pet name, etc. But this will require more effort and more time.

**apology.html** template is created to display **useful information for fields data validation** which user must know to input correct data.


- *Using sqlite3* to create database for this project named **pets.db**, its schema as following screenshot
![pets_DB_schema](./static/image/markdown_screenshots/pets_DB_schema.jpg)


### Summary:
You can find the link to this project here: **gitHub link** <https://github.com/code50/115123186/blob/3abb325530aec3d6665afcef22cc18c606c76548/project>
