<script>
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();
    let fileInput;

    function handleFileSelect() {
        const file = fileInput.files[0];
        if (!file) return;

        // Only accept image files
        if (!file.type.startsWith("image/")) {
            dispatch("error", "Please select an image file.");
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            dispatch("fileSelected", {
                file: file,
                previewUrl: e.target.result
            });
            console.log(previewUrl);
        };
        reader.readAsDataURL(file);
    }
    </script>

    <div class="form-control w-full">
    <label class="label">
        <span class="label-text">Choose an image file</span>
    </label>
    <input
        bind:this={fileInput}
        type="file"
        class="file-input file-input-bordered file-input-primary w-full mt-8"
        accept="image/*"
        on:change={handleFileSelect}
    />
</div>
