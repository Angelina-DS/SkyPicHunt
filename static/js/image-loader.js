export async function loadImageFromJson(endpointUrl, imgSelector, urlFieldName="url", hideUponError=false){
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