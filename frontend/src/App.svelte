<script>
    import { onMount } from 'svelte';
    import Header from './components/Header.svelte';
    import FileUpload from './components/FileUpload.svelte';
    import ImageCropModal from './components/ImageCropModal.svelte';

    let selectedFile = null;
    let previewUrl = '';
    let error = '';
    let mergedImage = null;
    let isEditing = false;

    let unique = {}

    function handleFileSelected(event) {
        selectedFile = event.detail.file;
        previewUrl = event.detail.previewUrl;
        error = '';
        isEditing = true;
    }

    function handleError(event) {
        error = event.detail;
    }

    function handleProcessedImage(event) {
        mergedImage = event.detail.mergedImage; // Get the merged image from the event
        isEditing = false;
    }

    function downloadImage() {
        const link = document.createElement('a');
        link.href = mergedImage;
        link.download = 'profile_with_banner.jpg';
        link.click();
    }

    function reEdit() {
        isEditing = true; // Reopen the modal for editing
    }

    export function resetApp() {
        unique = {}
        selectedFile = null; // Clear the selected file
        previewUrl = ''; // Clear the preview URL
        error = ''; // Clear any errors
        mergedImage = null; // Clear the merged image
        isEditing = false; // Close the modal
    }

</script>

<style>    
    .merged-image-container {
        text-align: center;
        margin-top: 20px;
    }

    .merged-image {
        object-fit: cover; /* Ensure the image fits the container */
        width: 300px;
        height: 300px;
        border: 1px solid #ccc;
        border-radius: 8px;
    }
</style>

<main class="flex flex-col items-center w-full mx-auto max-w-xl px-4 py-8">
    <div class="w-full">
        <Header title="Signal Banner App" />
        <div class="card bg-base-100 shadow-xl w-full">
            <div class="flex flex-col justify-center card-body">
                <h2 class="card-title">Upload photo:</h2>
                
                {#key unique}
                    <FileUpload 
                        on:fileSelected={handleFileSelected}
                        on:error={handleError}
                    />
                {/key}

                {#if isEditing && previewUrl}
                    <ImageCropModal 
                        {previewUrl}
                        on:error={handleError}
                        on:imageProcessed={handleProcessedImage}
                    />
                {/if}

                {#if error}
                    <div class="alert alert-error shadow-lg mt-4">
                        <div>
                            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                            <span>{error}</span>
                        </div>
                    </div>
                {/if}
            

            {#if mergedImage}
                <div class="flex flex-col items-center merged-image-container">
                    <h3 class="font-bold text-lg mb-4">Done!</h3>
                    <img src={mergedImage} alt="Merged Image" class="merged-image" />
                    <div class="flex flex-col gap-4 w-full max-w-xs mt-4">
                        <button class="btn btn-primary" on:click={downloadImage}>
                            Download Image
                        </button>
                        <button class="btn btn-error" on:click={reEdit}>
                            Edit some more
                        </button>
                        <button class="btn btn-secondary" on:click={resetApp}>
                            Reset
                        </button>
                    </div>
                </div>
            {/if}
            </div>
        </div>
    </div>
</main>