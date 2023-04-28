 fetch("/api/articles")
    .then(response => response.json())
    .then(function(response) {
        var container = document.querySelector('.cards')
        for (let article of response) {
            const card = document.createElement('div');
            card.classList.add('card');
            card.style.width = '18rem';

            const cardBody = document.createElement('div');
            cardBody.classList.add('card-body');

            const title = document.createElement('h5');
            title.classList.add('card-title');
            title.textContent = article.title;

            const subtitle = document.createElement('h6');
            subtitle.classList.add('card-subtitle', 'mb-2', 'text-body-secondary');
            subtitle.textContent = article.created_at;

            const text = document.createElement('p');
            text.classList.add('card-text');
            text.textContent = article.body;

            const deleteLink = document.createElement('a');
            deleteLink.classList.add('card-link');
            deleteLink.textContent = 'Delete';
            deleteLink.href = `/article/${article.id}/delete`;

            cardBody.appendChild(title);
            cardBody.appendChild(subtitle);
            cardBody.appendChild(text);
            cardBody.appendChild(deleteLink);
            card.appendChild(cardBody);
            container.appendChild(card);
            }
    })