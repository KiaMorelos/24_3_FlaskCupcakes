$cupcakeList = $("#cupcakes-list");
$cupcakeForm = $("#cupcake-form");
$searchForm = $("#search")
const apiURL = "http://localhost:5000/api/cupcakes";

function cupcakeMarkUp(cupcake){
    return `
    <li data-id="${cupcake.id}" class="list-group-item">
    <img src="${cupcake.image}" width="100">
    ${cupcake.flavor} | ${cupcake.size} | ${cupcake.rating}
    </li>`
}

async function showAllCupcakes() {
   $cupcakeList.empty()
   const res = await axios.get(apiURL);
   const {cupcakes} = res.data;
   
   for(let cupcake of cupcakes){
        htmlOfCupcake = cupcakeMarkUp(cupcake);
        $cupcakeList.append(htmlOfCupcake);
   }
}

async function showSearched(evt){
    evt.preventDefault();
    const search = $("#search-field").val()   
    const res = await axios.get(`${apiURL}/q=${search}`)
    
    if(res.data.message == "No Results"){
        $cupcakeList.empty()
        $cupcakeList.append(
            `<li class="list-group-item">No Results for: ${search}<br>
            <a href="/">Return to full list >></a>
            </li>
            `)
    }
    
    if (res.data.cupcakes) {
        $cupcakeList.empty()
        const {cupcakes} = res.data;
        for(let cupcake of cupcakes){
                htmlOfCupcake = cupcakeMarkUp(cupcake);
                $cupcakeList.append(htmlOfCupcake);
        }
        $cupcakeList.append(`<a href="/">Return to full list >></a>`)
    } 
}

async function newCupcake(evt){
    evt.preventDefault();
    
    const flavor = $("#flavor").val()
    const size = $("#size").val()
    const rating = $("#rating").val()
    const image = $("#image-url").val()
    
    const res = await axios.post(apiURL, {
        flavor,
        size,
        rating,
        image
    })
    
    const {cupcake} = res.data;
    htmlOfCupcake = cupcakeMarkUp(cupcake);
    $cupcakeList.append(htmlOfCupcake);
    $cupcakeForm.trigger("reset");
}

$cupcakeForm.on('submit', newCupcake);
$searchForm.on('submit', showSearched)

showAllCupcakes();
