<script>
    import { onMount, createEventDispatcher } from 'svelte';

    export let position = 0; // Initial position in percentage
    export let bannerHeight = 20; // Height of the banner in percentage
    export let opacity = 0.8;
    export let bannerUrl =  'banner.png'

    const dispatch = createEventDispatcher();
    let bannerElement;
    let aspectRatio = 1;

    let isDragging = false;
    let startY = 0; // Initial Y position of the mouse
    let initialPosition = 0; // Initial position of the banner

    onMount(async () => {
        // Load banner image to get its natural dimensions
        const img = new Image();
        img.src = bannerUrl;
        await img.decode();

        // Calculate aspect ratio
        aspectRatio = img.naturalWidth / img.naturalHeight;

        // Dynamically adjust the banner height to maintain aspect ratio
        const containerWidth = bannerElement.parentElement.offsetWidth; // Get the width of the parent container
        const calculatedHeight = containerWidth / aspectRatio; // Calculate height based on aspect ratio
        bannerHeight = (calculatedHeight / bannerElement.parentElement.offsetHeight) * 100; // Convert to percentage
    });

    function startDrag(event) {
        isDragging = true;
        startY = event.clientY; // Record the initial Y position of the mouse
        initialPosition = position; // Record the initial position of the banner
        window.addEventListener('mousemove', onDrag);
        window.addEventListener('mouseup', stopDrag);
    }

    function onDrag(event) {
        if (!isDragging) return;

        const deltaY = event.clientY - startY; // Calculate the vertical movement
        const containerHeight = bannerElement.parentElement.offsetHeight; // Get the height of the parent container
        const percentageDelta = (deltaY / containerHeight) * 100; // Convert movement to percentage

        // Update the position, ensuring it stays within bounds
        position = Math.min(Math.max(initialPosition + percentageDelta, 0), 100 - bannerHeight);
        dispatch('positionChange', position); // Emit the updated position
    }

    function stopDrag() {
        isDragging = false;
        window.removeEventListener('mousemove', onDrag);
        window.removeEventListener('mouseup', stopDrag);
    }
</script>

<style>
    .banner-overlay {
        position: absolute;
        left: 0;
        right: 0;
        width: 100%;
        cursor: grab; /* Indicate that the element can be dragged */
        background-size: 100% 100%;
        background-repeat: no-repeat;
        background-position: center;
        pointer-events: auto; /* Allow interaction with the banner */
    }

    .banner-overlay:active {
        cursor: grabbing; /* Change cursor when dragging */
    }
</style>

<div
    bind:this={bannerElement}
    class="banner-overlay"
    style="
        top: {position}%;
        height: {bannerHeight}%;
        opacity: {opacity};
        background-image: url('{bannerUrl}');
    "
    on:mousedown={startDrag}
></div>
