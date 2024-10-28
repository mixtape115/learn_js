const title = '速習react';
const price = '500';

const book = {title: title, price: price}
console.log(book)

const member1 = {
    name: '佐藤栞',
    greet: function(){
        console.log(`こんにちは${this.name}さん！`);
    }
}

const member2 = {
    name: '佐藤栞',
    greet(){
        console.log(`こんにちは${this.name}さん！`);
    }
}

let i = 0;
const member3 = {
    [`attr${++i}`]: '佐藤栞',
    [`attr${++i}`]: '女性',
    [`attr${++i}`]: '18歳',
};
console.log(member3);