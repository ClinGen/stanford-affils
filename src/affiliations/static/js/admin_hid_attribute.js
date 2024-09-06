document.addEventListener('DOMContentLoaded', function(){
    function toggleAffilID(value) {
      const affilIDWrapper = document.querySelector(".form-row.field-affiliation_id");
      if (value === "sibling") {
        affilIDWrapper.style.display = "block";
      } else {
        affilIDWrapper.style.display = "none";
      }
    }
      
    const affilRadioChoiceOne = document.querySelector('[id="id_affil_id_choice_0"]');
    if (affilRadioChoiceOne) {
        toggleAffilID(affilRadioChoiceOne.value);
    
        affilRadioChoiceOne.addEventListener("click", function(){
          toggleAffilID(this.value); })    
    }
  
    const affilRadioChoiceTwo = document.querySelector('[id="id_affil_id_choice_1"]');
    if (affilRadioChoiceTwo) {
        toggleAffilID(affilRadioChoiceTwo.value);
    
        affilRadioChoiceTwo.addEventListener("click", function(){
          toggleAffilID(this.value); })    
    }
  
    })
    