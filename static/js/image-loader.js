export async function loadImageFromJson(endpointUrl, imgSelector, urlFieldName="url", hideUponError=false, diffcTextID=null){
    const img = document.querySelector(imgSelector);
    if (!img) return console.error("Image element not found:", imgSelector);

    try{
        const res = await fetch(endpointUrl, {cache: "no-store"});
        if (!res.ok) {
            if (hideUponError)
                img.classList.add("hidden");
            throw new Error("Network error: "+res.status);
        }
        const data = await res.json();

        const ImageUrl = Array.isArray(data) ? data[0]?.[urlFieldName] : data?.[urlFieldName];

        //displaying difficulty
        if (diffcTextID != null){
            const imageDiffc = Array.isArray(data) ? data[0]?.["difficulty"] : data?.["difficulty"];
            let txt = "";
            for (let i=0; i<5; i++) txt+= "  "+ (i <= Math.floor(imageDiffc*5)? "\u2605" : "\u2606"); //&#x
            let diffcText = document.getElementById(diffcTextID);
            if (diffcText != null) diffcText.innerText = txt;
        }
        //displaying picture
        if (!ImageUrl) {
            if (hideUponError)
                img.classList.add("hidden");
            throw new Error("No image URL found in response");
        }

        img.addEventListener("load", ()=> {
            img.closest(".image-container")?.classList?.add("loaded");
        }, {once: true});

        img.addEventListener("error", ()=> {
            img.closest(".image-container")?.classList?.add("error");
            console.error("Failed to load image:", ImageUrl);
            if (hideUponError)
                img.classList.add("hidden");
        }, {once: true});

        img.src = ImageUrl;
    } catch (err) {
        console.error("loadImageFromJson error:", err);
        img?.closest(".image-container")?.classList?.add("error");
    }
}