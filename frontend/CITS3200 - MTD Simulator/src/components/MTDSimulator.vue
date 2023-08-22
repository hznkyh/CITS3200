<template>
    <header>
  <h2>MTD Simultor</h2>
</header>

<section>
  <form>
    <h2> Parameters Panel</h2>
  </form>
  
  <article>
    <h1>London</h1>
  </article>
</section>

<footer>
  <p>Footer</p>
</footer>
</template>

<script>
export default {
  name: 'MTDSimulator',
}
</script>

<style>
  * {
  box-sizing: border-box;
}

/* Style the header */
header {
  background-color: rgb(12, 69, 225);
  padding: 30px;
  text-align: center;
  font-size: 35px;
  color: white;
}

form {
  float: left;
  width: 30%;
  background: #ccc;
  padding: 20px;
}

article {
  float: left;
  padding: 20px;
  width: 70%;
  background-color: #f1f1f1;
  height: auto;
}

footer {
  background-color: #777;
  padding: 10px;
  text-align: center;
  color: white;
  position: absolute;
  bottom: 0;
  width: 100%;
}

@media (max-width: 600px) {
  form, article {
    width: 100%;
    height: auto;
  }
}

</style>