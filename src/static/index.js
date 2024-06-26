function handleEditClick(event) {
    const rowId = getRowId(event.srcElement.id);
    // Toggle visibilities of buttons.
    toggleVisible(event.srcElement.id);
    toggleVisible("cancel-button-"+rowId);

    // Get a NodeList Obj of all cells in the row that was selected.
    var cells = document.querySelectorAll("div[id$=" + CSS.escape(rowId) + "]");
    // Toggle div visibility.
    for (const cell of cells) {
        toggleVisible(cell.id);
    }
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
    toggleVisible("edit-button-"+rowId);

    // Get a NodeList Obj of all cells in the row that was selected.
    var cells = document.querySelectorAll("div[id$=" + CSS.escape(rowId) + "]");
    // Toggle div visibility.
    for (const cell of cells) {
        toggleVisible(cell.id);
    };
};

// Get a NodeList Obj of all cancel buttons, add EventListener to each.
var cancelButtons = document.querySelectorAll("button[id^='cancel-button-']");
for (const cancelButton of cancelButtons) {
    cancelButton.addEventListener("click", handleCancelClick);
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