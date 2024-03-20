const comments = document.querySelectorAll('.comment');
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    const commentsToShow = 3;
    let currentShownIndex = commentsToShow;

    // Скрыть все комментарии, начиная с 4-го
    for (let i = currentShownIndex; i < comments.length; i++) {
        comments[i].style.display = 'none';
    }

    loadMoreBtn.addEventListener('click', function() {
        for (let i = currentShownIndex; i < currentShownIndex + commentsToShow && i < comments.length; i++) {
            comments[i].style.display = 'block';
        }
        currentShownIndex += commentsToShow;

        if (currentShownIndex >= comments.length) {
            loadMoreBtn.style.display = 'none'; // Скрыть кнопку после загрузки всех комментариев
        }
    });