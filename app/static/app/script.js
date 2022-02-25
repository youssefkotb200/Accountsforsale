document.addEventListener('DOMContentLoaded', () => {
    let rightarrow = document.getElementsByClassName('right_arrow')
    let leftarrow = document.getElementsByClassName('left_arrow')
    let products = document.getElementsByClassName('product_body')
    let slidebar = document.getElementsByClassName('prod_1')
    for (let i = 0; i < leftarrow.length; i++) {
        leftarrow[i].addEventListener('click', () => {
            slidebar[i].scrollLeft -= 280;        
        })
        rightarrow[i].addEventListener('click', () => {
            slidebar[i].scrollLeft += 280; 
        })
    }
    let maxscrollleft = []
    for (let i = 0; i < slidebar.length; i++) {
         maxscrollleft.push(slidebar[i].scrollWidth - slidebar[i].clientWidth)

    }
    function autoplay() {
        for ( let i = 0; i < slidebar.length; i++) {
            if (slidebar[i].scrollLeft > (maxscrollleft[i] - 1)) {
                slidebar[i].scrollLeft -= maxscrollleft[i]
            }
            else {
                slidebar[i].scrollLeft += 1
            }
        }
    }
    for( let i = 0; i < products.length; i++) {
        products[i].addEventListener('mouseover', () => {
            clearInterval(play)
        })
        products[i].addEventListener('mouseout', () => {
            return play = setInterval(autoplay, 50)
        })
    }


    let play = setInterval(autoplay, 50)

    //Get the button
    let mybutton = document.getElementById("btn-back-to-top");

    // When the user scrolls down 20px from the top of the document, show the button
    window.onscroll = function () {
    scrollFunction();
    };

    function scrollFunction() {
        if (
            document.body.scrollTop > 20 ||
            document.documentElement.scrollTop > 20
        ) {
            mybutton.style.display = "block";
        } else {
            mybutton.style.display = "none";
        }
    }
    // When the user clicks on the button, scroll to the top of the document
    mybutton.addEventListener("click", backToTop);

    function backToTop() {
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
    }
})

