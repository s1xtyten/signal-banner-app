<script>
    import { createEventDispatcher } from 'svelte';
    import Cropper from 'svelte-easy-crop';
    import Banner from './Banner.svelte'
    import { imageSettings } from '../stores/imageStore';

    export let previewUrl;

    const dispatch = createEventDispatcher();
    const API_BASE_URL = 'http://127.0.0.1:5000';

    // Component state
    let step = 1;
    let zoom = 1; // Zoom level
    let crop;
    let croppedImage = null;
    let croppedAreaPixels = null; // Cropped area in pixels
    let isModalOpen = false;
    let isLoading = false;
    let position = $imageSettings.bannerPosition;
    let bannerHeight = 20; // Percentage of image height
    let bannerUrl = '/assets/banner.png'
    let mergedImage = null;

    let sliderOpacity = $imageSettings.bannerOpacity * 100; // Slider value (0-100)
    $: opacity = sliderOpacity / 100; // Convert slider value to decimal (0-1)

    $: if (previewUrl) {
        isModalOpen = true;
    }

    function onCropComplete(event) {
        croppedAreaPixels = event.detail.pixels;
    }

    async function generateCroppedImage() {
    if (!croppedAreaPixels) {
        console.warn('Cropped area is not defined. Triggering onCropComplete manually.');
        onCropComplete({ detail: { pixels: { x: 0, y: 0, width: 100, height: 100 } } }); // Default crop area
    }

    try {
        const canvas = document.createElement('canvas');
        const image = new Image();
        image.src = previewUrl;

        await new Promise((resolve) => (image.onload = resolve));

        const ctx = canvas.getContext('2d');

        // Set the canvas size to match the cropped area
        canvas.width = croppedAreaPixels.width;
        canvas.height = croppedAreaPixels.height;

        // Draw the cropped portion of the image onto the canvas
        ctx.drawImage(
            image,
            croppedAreaPixels.x, // Source X
            croppedAreaPixels.y, // Source Y
            croppedAreaPixels.width, // Source Width
            croppedAreaPixels.height, // Source Height
            0, // Destination X
            0, // Destination Y
            canvas.width, // Destination Width
            canvas.height // Destination Height
        );

        // Convert the canvas content to a data URL
        croppedImage = canvas.toDataURL('image/jpeg');
        step = 2; // Move to Step 2
    } catch (err) {
        console.error('Error generating cropped image:', err);
    }
}

async function processImage() {
        if (!croppedAreaPixels) {
            console.error('Cropped area is not defined.');
            return;
        }

        isLoading = true;
        try {
            // Set fixed canvas dimensions (e.g., 1000x1000 for high resolution)
            const canvasWidth = 800; // Fixed width
            const canvasHeight = 800; // Fixed height
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');

            canvas.width = canvasWidth;
            canvas.height = canvasHeight;
            
            // Load image
            const croppedImg = new Image();
            croppedImg.src = croppedImage;
            await new Promise((resolve) => (croppedImg.onload = resolve));

            // Draw the cropped image
            ctx.drawImage(croppedImg, 0, 0, canvas.width, canvas.height);

            const bannerImg = new Image();
            bannerImg.src = bannerUrl; // Use the banner image URL
            await new Promise((resolve) => (bannerImg.onload = resolve));

            const bannerHeightPx = (bannerHeight / 100) * canvas.height;
            const bannerY = (position / 100) * canvas.height;

            ctx.globalAlpha = opacity; // Set banner opacity
            ctx.drawImage(bannerImg, 0, bannerY, canvas.width, bannerHeightPx);

            // Convert the canvas content to a data URL
            mergedImage = canvas.toDataURL('image/jpeg');

            // Emit the merged image to the parent component
            dispatch('imageProcessed', { mergedImage });

            // Close the modal
            closeModal();
                } catch (err) {
                    console.error('Error processing image:', err);
                } finally {
                    isLoading = false;
                }
    }

    function closeModal() {
        isModalOpen = false;
        dispatch('close');
    }
</script>

<style>
    .cropper-container {
        position: relative;
        width: 100%;
        height: 400px;
        background-color: #333;
        overflow: hidden;
    }

    .cropped-image-container {
        display: flex; 
        position: relative;
        width: 100%;
        height: 400px;
        background-color: #333;
        overflow: hidden;
        margin: auto;
    } 

    .cropped-image {
        width: 100%;
        height: 400px;
        object-fit: cover; 
    } 
</style>

<div class="modal modal-open" class:modal-open={isModalOpen}>
    <div class="modal-box max-w-4xl">
        {#if step === 1}
            <h3 class="font-bold text-lg mb-4">Crop your photo</h3>
            <p class="font-normal text-xs">Just scroll or adjust slider to zoom, click and drag to move</p>      
        {:else if step === 2}
            <h3 class="font-bold text-lg mb-4">Adjust banner</h3>
            <p class="font-normal text-xs">Just click and drag to place it where you like and change the opacity with the slider</p>
        {/if}
        
        <div class="flex flex-col items-center">    
            {#if step === 1}
                <!-- Step 1: Crop Image -->
                <div class="cropper-container">
                    <Cropper
                        crop={crop}
                        image={previewUrl}
                        zoom={zoom}
                        aspect={1}
                        cropSize={{ width: 300, height: 300 }} 
                        on:cropchange={(newCrop) => (crop = newCrop)}
                        on:zoomchange={(newZoom) => (zoom = newZoom)}
                        on:cropcomplete={onCropComplete}
                    />
                </div>

                <div class="form-control mt-4">
                    <label class="label">
                        <span class="label-text">Zoom</span>
                        <span class="label-text-alt">{Math.round(zoom * 100)}%</span>
                    </label>
                    <input
                        type="range"
                        min="1"
                        max="3"
                        step="0.1"
                        bind:value={zoom}
                        class="range range-primary"
                    />
                </div>

                <div class="modal-action">
                    <button class="btn btn-error" on:click={closeModal}>
                        Cancel
                    </button>
                    <button class="btn btn-primary" on:click={generateCroppedImage}>
                        Next: Add Banner
                    </button>
                </div>
            {:else if step === 2}
                <!-- Step 2: Adjust Banner -->
                <div 
                    class="cropped-image-container flex flex-col items-center"
                >
                    <img src={croppedImage} alt="Cropped Image" class="cropped-image" />

                    <Banner
                        bind:position
                        bind:opacity
                        {bannerHeight}
                    />
                </div>
                <div class="form-control mt-4">
                    <label class="label">
                        <span class="label-text">Banner Opacity</span>
                        <span class="label-text-alt">{Math.round(sliderOpacity)}%</span>
                    </label>
                    <input
                        type="range"
                        min="0"
                        max="100"
                        bind:value={sliderOpacity}
                        class="range range-primary"
                    />
                </div>

                <div class="modal-action">
                    <button class="btn btn-error" on:click={closeModal}>
                        Cancel
                    </button>
                    <button class="btn btn-secondary" on:click={() => (step = 1)}>
                        Back
                    </button>
                    <button class="btn btn-primary" on:click={processImage} disabled={isLoading}>
                        {#if isLoading}
                            <span class="loading loading-spinner"></span>
                            Processing...
                        {:else}
                            I'm done!
                        {/if}
                    </button>
                </div>
            {/if}
        </div>
    </div>
</div>
