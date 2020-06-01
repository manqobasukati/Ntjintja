// Init F7 Vue Plugin

Vue.use(Framework7Vue)



vm = new Vue({
	el:"#app",
	framework7:{
		root:"#app",
		material: true,
		

	},
	data:{
	  
	  done:[]
	},
	methods:{
	  dialFunction:function(i){
		  
		  var self = this;
		  if(i.dialled === false){
			 
			
			console.log("Not dialled");
			phonedialer.dial(
				encodeURIComponent("*141*"+i.resent_amount+"*"+i.to_number+"#"), 
				function(err) {
				
					if (err == "empty") 
					{
						alert("Unknown phone number")
					}else {
						alert("Dialer Error:" + err)
					};    
				},
				function(success) { 
					alert('Dialing succeeded');
				}
			);
			
			$.ajax({
				type:"PUT",
				url:"http://manqoba.pythonanywhere.com/transactions/"+i.id,
				//url:"http://127.0.0.1:5000/transactions/"+i.id,
				success:function(){
					console.log("Updated");
				}
			});
		  }else{
			  console.log("Dialled");
		  }
	  },
	  check:function(){
		  var self = this;
		  $.ajax({
			  type:"GET",
			  url:"http://manqoba.pythonanywhere.com/transactions/swazi-mobile",
			  //url:"http://127.0.0.1:5000/transactions/swazi-mobile",
			  success:function(data){
				  console.log(data.output.length)
				  for(var i = 0;i <= data.output.length -1; i++){
					 
					 console.log(data.output[i]);
					 
					 self.dialFunction(data.output[i]);
					
				  }
				  
				 
				  
				  
				 
				  
			
			  }
		  });
		  
		  console.log("Just checking");
	  },
	  
  }
});

vm.check();


setInterval(function(){
	vm.check();
},30000)

