$(document).ready(function() {
    // Account menu toggle
    $('#accountBtn').click(function() {
        $('#accountMenu').toggle();
    });
    
    // File upload handling
    $('#uploadBox').click(function() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.ppt,.pptx,.pdf';
        
        input.onchange = e => {
            const file = e.target.files[0];
            if (file) {
                localStorage.setItem('uploadedPPT', file.name);
                $('#uploadBox').text(`Uploaded: ${file.name}`);
                $('#uploadBox').css('background-color', 'var(--first-color-alt)');
            }
        }
        
        input.click();
    });
    
    // Character selection
    $('.character-card').click(function() {
        $('.character-card').removeClass('selected');
        $(this).addClass('selected');
        localStorage.setItem('selectedCharacter', $(this).data('char'));
    });
});