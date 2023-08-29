<template>
    <div>
      <header>
        <h2>Home</h2>
      </header>
    </div>
    <p>This is a test sentence.</p>
    <p>This is a test sentence.</p>
    <p>This is a test sentence.</p>
    <p>This is a test sentence.</p>
    <p>This is a test sentence.</p>
    <p>This is a test sentence.</p>
    <footer></footer>
</template>

<script>
export default {
  name: 'Home',
}
</script>

<style>
header {
  background-color: rgb(12, 69, 225);
  padding: 30px;
  text-align: center;
  font-size: 35px;
  color: white;
}
footer {
  flex-shrink: 0;
  background-color: #777;
  text-align: center;
  color: white;
  bottom: 0;
  padding: 10px;
}
</style>