console.log("rent.js loaded");
document.addEventListener("DOMContentLoaded", async ()=>{
   const rent_list = document.getElementById("rent-list");
   console.log(rent_list);

let rents = [];
try {
    const respond = await fetch ("/api/my-rents/",{
        headers: {"Accept": "application/json"},
    })
    if(!respond.ok){
        rent_list.innerHTML = `<p>Fail to load rents with code : ${respond.status}</p>`
        return;
    }
    rents = await respond.json();
    render(rents);
}
catch (err){
    rents.innerHTML ="<p>Failed to load cars. Something happend with Api.</p>";
    return;
}
function render(list){
    rent_list.innerHTML = "";
    if(!list.length){
        rent_list.innerHTML = "<p>No rents at the moment :[</p>";
        return;

    }
    for(const offer of list){
        const card =  document.createElement("div");
        card.className = "card";
        card.innerHTML = `
        <h3>${offer.car.brand} ${offer.car.model}</h3>
         <p>
          Pickup Location: ${offer.pickup_location.name} ${offer.pickup_location.city} ${offer.pickup_location.address}<br>
          Drop off Location: ${offer.dropoff_location.name} ${offer.dropoff_location.city} ${offer.dropoff_location.address}<br>
          start_date: ${offer.start_date}<br>
          end_date: ${offer.end_date}<br>
          total_price: ${offer.total_price}$<br>
          status: ${offer.status}
        </p>
              
`;
        if(offer.status === "pending"){
            card.innerHTML+=`<a href=\"${offer.id}/delete">Cancel  </a>  <a href="${offer.id}/edit"> Edit</a>`

        }
        rent_list.appendChild(card);
    }
}


});