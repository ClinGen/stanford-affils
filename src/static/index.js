function handleEditClick(event) {
    const rowId = getRowId(event.srcElement.id);
    // Toggle visibilities of buttons.
    toggleVisible("cancel-button-"+rowId);
    toggleAllOfSame("button[id^='edit-button-']");
    toggleAllOfSame("button[id^='submit-button-" + CSS.escape(rowId) + "']");
    toggleAllOfSame("div[id$=" + CSS.escape(rowId) + "]");
};

// Get a NodeList Obj of all edit buttons, add EventListener to each.
var editButtons = document.querySelectorAll("button[id^='edit-button-']");
for (const editButton of editButtons) {
    editButton.addEventListener("click", handleEditClick);
};

function handleCancelClick(event) {
    const rowId = getRowId(event.srcElement.id);
    // Toggle visibilities of buttons.
    toggleVisible(event.srcElement.id);
    toggleAllOfSame("button[id^='edit-button-']");
    toggleAllOfSame("button[id^='submit-button-" + CSS.escape(rowId) + "']");
    toggleAllOfSame("div[id$=" + CSS.escape(rowId) + "]");

    // Replace cancelled input text with existing cell text.
    var allInputs = document.querySelectorAll("input");
    var allTextCells = document.querySelectorAll("div[id$='cell-text-" + CSS.escape(rowId) + "']");
    for (let i = 0; i < allTextCells.length; i++) {
        allInputs[i].value = allTextCells[i].textContent.trim();
    };
};

// Get a NodeList Obj of all cancel buttons, add EventListener to each.
var cancelButtons = document.querySelectorAll("button[id^='cancel-button-']");
for (const cancelButton of cancelButtons) {
    cancelButton.addEventListener("click", handleCancelClick);
};

function handleSubmitClick(event) {
    const rowId = getRowId(event.srcElement.id);
    // Toggle visibilities of buttons.
    toggleVisible(event.srcElement.id);
    toggleAllOfSame("button[id^='edit-button-']");
    toggleAllOfSame("button[id^='cancel-button-" + CSS.escape(rowId) + "']");
    toggleAllOfSame("div[id$=" + CSS.escape(rowId) + "]");

    // Replace cancelled input text with existing cell text.
    var allInputs = document.querySelectorAll("input");
    var allTextCells = document.querySelectorAll("div[id$='cell-text-" + CSS.escape(rowId) + "']");
    for (let i = 0; i < allTextCells.length; i++) {
        allTextCells[i].textContent = allInputs[i].value;
    };
};
// Get a NodeList Obj of all cancel buttons, add EventListener to each.
var submitButtons = document.querySelectorAll("button[id^='submit-button-']");
for (const submitButton of submitButtons) {
    submitButton.addEventListener("click", handleSubmitClick);
};

// Helper function to get rowId.
function getRowId(idName) {
    const rowId = idName.slice(idName.lastIndexOf("-") + 1,idName.length);
    return rowId;
};

// Helper function to toggle visibility.
function toggleVisible(idName) {
    var x = document.getElementById(idName)
        if (x.style.display === "none") {
            x.style.display = "block";
        } else {
            x.style.display = "none";
        }
};

function toggleAllOfSame(identifier) {
    var idNodeListObj = document.querySelectorAll(identifier);
    for (const item of idNodeListObj) {
        toggleVisible(item.id);
    };
};