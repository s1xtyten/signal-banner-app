<script>
    import { createEventDispatcher } from 'svelte';

    export let position = 0; // Initial position in percentage
    export let bannerHeight = 20; // Height of the banner in percentage
    export let opacity = 1;
    export let bannerUrl =  '/assets/banner.png'

    const dispatch = createEventDispatcher();

    let isDragging = false;
    let startY = 0; // Initial Y position of the mouse
    let initialPosition = 0; // Initial position of the banner

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
        const containerHeight = 300; // Height of the container (in pixels)
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
        cursor: grab; /* Indicate that the element can be dragged */
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        pointer-events: auto; /* Allow interaction with the banner */
    }

    .banner-overlay:active {
        cursor: grabbing; /* Change cursor when dragging */
    }
</style>

<div
    class="banner-overlay"
    style="
        top: {position}%;
        height: {bannerHeight}%;
        opacity: {opacity};
        background-image: url('{bannerUrl}');
    "
    on:mousedown={startDrag}
></div>
