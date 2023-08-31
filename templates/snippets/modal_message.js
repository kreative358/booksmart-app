
const modal_message = () => {   
  
      console.clear();
      var mymodal_main = document.getElementById("mymodal_messages_main");
      var mymodal_cont_main = document.getElementById("modal_cont_messages_main");
  
        mymodal_main.style.display = "block";
        mymodal_main.style.animation = "modalfadein 1s 1";
        
        mymodal_main.src = this.src;
        mymodal_cont_main.style.display = "block"; 
        mymodal_cont_main.style.animation = "zoom 2s 1 ease-in"; 
        mymodal_cont_main.src = this.src;
        var span1 = document.getElementsByClassName("close_m")[0];
        var span2 = document.getElementsByClassName("close_mb")[0];
        span1.onclick = function() {
          mymodal_cont_main.style.animation = "unzoom 2s 1";
          mymodal_main.style.animation = "modalfadeout 1s 1 1s";
          setTimeout(()=> {
            mymodal_cont_main.style.display = "none";
            mymodal_main.style.display = "none"
              }
              , 1900);
        }        
        
        span2.onclick = function() {
          mymodal_cont_main.style.animation = "animatetopback 2s 1";
          mymodal_main.style.animation = "modalfadeout 1s 1 1s";
          setTimeout(()=> {
            mymodal_cont_main.style.display = "none";
            mymodal_main.style.display = "none"
              }
              , 1900);
        }
    
            mymodal_main.onclick = function() {
            mymodal_cont_main.style.animation = "unzoomrotate 2s 1";
            mymodal_main.style.animation = "modalfadeout 1s 1 1s";
            setTimeout(()=> {
            mymodal_cont_main.style.display = "none";
            mymodal_main.style.display = "none"
              }, 1900);
      
          }
        }
      export default modal_message;
     


       


