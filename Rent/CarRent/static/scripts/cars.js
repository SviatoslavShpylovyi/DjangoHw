console.log("cars.js loaded");
document.addEventListener("DOMContentLoaded", async ()=>{
const search = document.getElementById("car-search-js");
const card_list = document.getElementById("cars-list-js");
console.log(search);
console.log(card_list);

    if(!search || !card_list) return;
search.addEventListener("input",()=>{
   const val = search.value.trim().toLowerCase();
   if(!val){
       render(cars);
       return;
   }
   const filter = cars.filter((c)=>{
      const text = `${c.brand} ${c.model}`.toLowerCase();
      return text.includes(val);
   });
   render(filter);
});






let cars = [];
try {
    const respond = await fetch ("/api/cars/",{
        headers: {"Accept": "application/json"},
    })
    if(!respond.ok){
        card_list. innerHTML = `<p>Fail to load cars with code : ${respond.status}</p>`
        return;
    }
    cars = await respond.json();
    render(cars);
}
catch (err){
    card_list.innerHTML ="<p>Failed to load cars. Something happend with Api.</p>";
    return;
}


function render(list){
    card_list.innerHTML = "";
    if(!list.length){
        card_list.innerHTML = "<p>No cars found</p>";
        return;

    }
    for(const car of list){
        const img = car.image
  ? `<img class="car-img" src="${car.image}" alt="${car.brand} ${car.model}">`
  : `<div class="car-img-placeholder">No image</div>`
        const card =  document.createElement("div");
        card.className = "card";
        card.innerHTML = `
        ${img}
        <h3>${car.brand} ${car.model}</h3>
         <p>
          Year: ${car.year}<br>
          Price/day: ${car.daily_price}<br>
          Transmission: ${car.transmission}<br>
          Fuel: ${car.fuel_type}<br>
          Seats: ${car.seats}
        </p>        
        <a href="${car.id}">Details</a>

        
        
        `;
        card_list.appendChild(card);
    }
}

render(cars);


});