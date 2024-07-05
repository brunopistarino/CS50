document.addEventListener('DOMContentLoaded', function() {

    document.querySelector("#all-posts").addEventListener('click', () => all_posts());

    document.querySelector("#create-form").onsubmit = () => create_post();
    document.querySelector("#create-close").addEventListener('click', () => {
        document.querySelector("#create-view").style.display = 'none';
        document.querySelector("#pagination-view").style.display = 'block';
    });
    document.querySelector("#create-button").addEventListener('click', () => {document.querySelector("#pagination-view").style.display = 'block';});
    
    document.addEventListener('keyup', () => {
        if(document.querySelector("#create-content").value === "") {
            document.querySelector("#create-button").setAttribute("disabled", true);
        } else {
            document.querySelector("#create-button").removeAttribute("disabled");
        }
    })

    fetch('/authentication')
    .then(response => response.json())
    .then(authentication => {
        if(authentication.authentication === true) {
            document.querySelector("#following-posts").addEventListener('click', () => following_posts());
            document.querySelector("#create-post").addEventListener('click', () => show_window("create"));
            document.querySelector("#left-username").addEventListener('click', () => load_profile(document.querySelector("#left-username-text").innerHTML));
            document.querySelector("#bottom").style.display = "grid";
        }
    })

    all_posts();
});

function all_posts(current_page_number) {
    if(current_page_number == null) {
        current_page_number = 1
    }

    document.querySelector("#pagination-container").innerHTML = "";
    document.querySelector("#posts-view").innerHTML = "";

    document.querySelector("#profile-view").style.display = 'none';

    const section_title = document.createElement("h1");
    section_title.className = "section-title";
    section_title.innerHTML = "All Posts";
    document.querySelector("#posts-view").appendChild(section_title);

    fetch(`/posts/${current_page_number}`)
    .then(response => response.json())
    .then(posts => {
        load_posts(posts)
        pagination(posts, "all_posts")
    });
}

function following_posts(current_page_number) {
    if(current_page_number == null) {
        current_page_number = 1
    }

    document.querySelector("#profile-view").style.display = 'none';
    document.querySelector("#pagination-container").innerHTML = "";
    document.querySelector("#posts-view").innerHTML = "";

    const section_title = document.createElement("h1");
    section_title.className = "section-title";
    section_title.innerHTML = "Following";
    document.querySelector("#posts-view").appendChild(section_title);

    fetch(`/following/${current_page_number}`)
    .then(response => response.json())
    .then(posts => {
        load_posts(posts)
        pagination(posts, "following")
    });
}

function load_posts(posts) {
    document.querySelector("#create-view").style.display = 'none';
    document.querySelector("#posts-view").style.display = 'block';
    document.querySelector("#pagination-container").innerHTML = "";

    posts.posts.forEach((post) => {
        const container = document.createElement("div");
        const profile_name = document.createElement("a");
        const content = document.createElement("p");
        const timestamp = document.createElement("p");
        const top_div = document.createElement("div");
        const likes_div = document.createElement("div")
        const likes = document.createElement("p");
        const like_icon = document.createElement("i");
            
        container.className = "post";
        profile_name.className = "post-name clickeable";
        content.className = "post-content";
        timestamp.className = "post-timestamp";
        top_div.className = "post-top-div"
        likes_div.className = "post-likes-div";
        likes.className = "post-likes";

        fetch(`/like/state/${post.id}`)
        .then(response => response.json())
        .then(like => {
            if(like.state === true) {
                like_icon.classList = "post-like-icon fas red fa-heart";
            } else {
                like_icon.className = "post-like-icon far fa-heart";
            }
        });

        profile_name.innerHTML = post.user;
        content.innerHTML = post.content;
        timestamp.innerHTML = post.timestamp;
        likes.innerHTML = post.likes;

        profile_name.addEventListener('click', () => load_profile(post.user));
        like_icon.addEventListener('click', () => like(like_icon, likes, post));

        fetch(`edit/${post.id}/1`)
        .then(response => response.json())
        .then(edit => {
            if(edit.owner === true) {
                const edit_button = document.createElement("a");
                edit_button.className = "post-edit clickeable";
                edit_button.innerHTML = "Edit";
                edit_button.addEventListener('click', () => edit_post(post.id, content, edit_button));
                top_div.appendChild(edit_button);
            }
        });

        container.appendChild(top_div);
        top_div.appendChild(profile_name);
        top_div.appendChild(timestamp);
        container.appendChild(content);
        container.appendChild(likes_div);
        likes_div.appendChild(like_icon);
        likes_div.appendChild(likes);
        document.querySelector("#posts-view").appendChild(container);
    });
}

function load_profile(user, current_page_number) {
    if(current_page_number == null) {
        current_page_number = 1
    }

    document.querySelector("#profile-view").style.display = 'block';
    document.querySelector("#profile-view").innerHTML = "";
    document.querySelector("#posts-view").innerHTML = "";

    fetch(`/profile/${user}/${current_page_number}`)
    .then(response => response.json())
    .then(profile => {
        const username = document.createElement("h1");
        const follows_div = document.createElement("div");
        const following = document.createElement("p");
        const followers = document.createElement("p");

        username.className = "profile-username";
        follows_div.className = "profile-follows-div";
        following.className = "profile-follows";
        followers.className = "profile-follows";

        username.innerHTML = profile.username;
        following.innerHTML = `${profile.following} Following`;
        followers.innerHTML = `${profile.followers} Followers`;

        document.querySelector("#profile-view").appendChild(username);
        document.querySelector("#profile-view").appendChild(follows_div);
        follows_div.appendChild(following);
        follows_div.appendChild(followers);

        fetch('/authentication')
        .then(response => response.json())
        .then(authentication => {
            if(authentication.authentication === true && profile.current_user !== profile.username) {
                const follow_button = document.createElement("a");
                follow_button.className = "clickeable profile-follows-btn";
                if(profile.check_follow === true) {
                    follow_button.innerHTML = "Unfollow";
                } else {
                    follow_button.innerHTML = "Follow";
                }
                follow_button.addEventListener('click', () => follow(profile, followers, follow_button));
                follows_div.appendChild(follow_button);
            }
        })

        load_posts(profile);
        pagination(profile, "profile", user);
    })
}

function create_post() {
    fetch('/posts/create', {
        method: 'POST',
        body: JSON.stringify({
            content: document.querySelector("#create-content").value
        })
    })
    .then(() => all_posts());
    return false;
}

function show_window(window_id) {
    document.querySelector("#create-button").setAttribute("disabled", true);
    const window = document.getElementById(`${window_id}-view`);
    
    window.style.display = 'block';
    document.querySelector("#pagination-view").style.display = 'none';
    document.getElementById(`${window_id}-content`).value = "";

    document.getElementById("create-content").focus();

    window.addEventListener('click', function(e){   
        if (!document.getElementById(`${window_id}-container`).contains(e.target)) {
            window.style.display = 'none';
            document.querySelector("#pagination-view").style.display = 'block';
        }
      });
}

function like(like_icon, likes, post) {
    fetch(`/like/${post.id}`)
    .then(response => response.json())
    .then(amount => {
        if(like_icon.classList.contains("far")) {
            like_icon.classList.remove("far");
            like_icon.classList.add("fas");
            like_icon.classList.add("red");
            likes.innerHTML = amount.amount;
        } else {
            like_icon.classList.remove("fas");
            like_icon.classList.remove("red");
            like_icon.classList.add("far");
        };
        likes.innerHTML = amount.amount;
    })
}

function follow(profile, followers, follow_button) {
    fetch(`/follow/${profile.username}`)
    .then(response => response.json())
    .then(follow => {
        if(follow.state === false) {
            follow_button.innerHTML = "Unfollow";
        } else {
            follow_button.innerHTML = "Follow";
        }
        followers.innerHTML = `${follow.followers} Followers`;
    })
}

function edit_post(post_id, content, edit_button) {
    const original_content = content.innerHTML;

    const edit_content = document.createElement("textarea");
    const edit_save_button = document.createElement("a")

    edit_content.className = "edit-content";
    edit_save_button.className = "edit-save-button post-edit clickeable";

    edit_content.value = original_content;
    edit_save_button.innerHTML = "Save";

    content.replaceWith(edit_content);
    edit_button.replaceWith(edit_save_button);

    edit_content.focus();

    edit_save_button.addEventListener('click', () => {
        if(edit_content.value !== "") {
            fetch(`/edit/${post_id}/2`, {
                method: 'PUT',
                body: JSON.stringify({
                    content: edit_content.value
                })
            })
            .then(() => {
                edit_content.replaceWith(content);
                edit_save_button.replaceWith(edit_button);
                content.innerHTML = edit_content.value;
            });
        }
    })
}

function pagination(posts, type, user) {
    const prev = posts.has_previous;
    var current = posts.current_page_number;
    const next = posts.has_next;
    const container = document.querySelector("#pagination-container");

    if(prev === true) {
        prev_buttom = document.createElement("li");
        prev_buttom.className = "page-item";
        prev_buttom.innerHTML = `<a class="page-link clickeable"><i class="fas fa-arrow-left"></i></a>`;
        container.append(prev_buttom);

        if(type === "all_posts") {
            prev_buttom.addEventListener('click', () => all_posts(--current))
        } else if(type === "following") {
            prev_buttom.addEventListener('click', () => following_posts(--current))
        } else if(type === "profile") {
            prev_buttom.addEventListener('click', () => load_profile(user, --current))
        }
    }

    current_page = document.createElement("li");
    current_page.className = "page-item";
    current_page.innerHTML = `<a class="page-link">${current}</a>`;
    container.append(current_page);

    if(next === true) {
        next_buttom = document.createElement("li");
        next_buttom.className = "page-item";
        next_buttom.innerHTML = `<a class="page-link clickeable"><i class="fas fa-arrow-right"></i></a>`;
        container.append(next_buttom);

        if(type === "all_posts") {
            next_buttom.addEventListener('click', () => all_posts(++current))
        } else if(type === "following") {
            next_buttom.addEventListener('click', () => following_posts(++current))
        } else if(type === "profile") {
            next_buttom.addEventListener('click', () => load_profile(user, ++current))
        }
    }
}