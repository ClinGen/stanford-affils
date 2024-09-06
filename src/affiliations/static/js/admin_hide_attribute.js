document.addEventListener('DOMContentLoaded', function(){
    function toggleAffilID(value) {
      const affilIDWrapper = document.querySelector(".form-row.field-sib_affil_id_choices");
      if (value === "sibling") {
        affilIDWrapper.style.display = "block";
      } else {
        affilIDWrapper.style.display = "none";
      }
    }
      
    const affilRadioChoiceOne = document.querySelector('input[id="id_affil_id_type_choice_0"]');
    if (affilRadioChoiceOne) {
        toggleAffilID(affilRadioChoiceOne.value);
    
        affilRadioChoiceOne.addEventListener("click", function(){
          toggleAffilID(this.value); })    
    }
  
    const affilRadioChoiceTwo = document.querySelector('input[id="id_affil_id_type_choice_1"]');
    if (affilRadioChoiceTwo) {
    
        affilRadioChoiceTwo.addEventListener("click", function(){
          toggleAffilID(this.value); })    
    }
  
    })
    