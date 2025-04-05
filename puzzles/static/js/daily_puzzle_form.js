document.addEventListener('DOMContentLoaded', function () {
  const menuSelect = document.getElementById('id_menu');
  const categorySelect = document.getElementById('id_category');
  const levelSelect = document.getElementById('id_level');
  const puzzleSelect = document.getElementById('id_puzzle');

  if (menuSelect) {
    menuSelect.addEventListener('change', function () {
      const menuId = this.value;
      fetch(`/adminapi/categories/?menu_id=${menuId}`)
        .then(response => response.json())
        .then(data => {
          categorySelect.innerHTML = '<option value="">---------</option>';
          data.forEach(category => {
            const option = document.createElement('option');
            option.value = category.id;
            option.textContent = category.name;
            categorySelect.appendChild(option);
          });
          // Clear dependent dropdowns
          levelSelect.innerHTML = '<option value="">---------</option>';
          puzzleSelect.innerHTML = '<option value="">---------</option>';
        });
    });
  }

  if (categorySelect) {
    categorySelect.addEventListener('change', function () {
      const categoryId = this.value;
      fetch(`/adminapi/levels/?category_id=${categoryId}`)
        .then(response => response.json())
        .then(data => {
          levelSelect.innerHTML = '<option value="">---------</option>';
          data.forEach(level => {
            const option = document.createElement('option');
            option.value = level.levelNumber;
            option.textContent = level.display_name;
            levelSelect.appendChild(option);
          });
          // Clear dependent dropdown
          puzzleSelect.innerHTML = '<option value="">---------</option>';
        });
    });
  }

  if (levelSelect) {
    levelSelect.addEventListener('change', function () {
      const levelId = this.value;
      fetch(`/adminapi/puzzles/?level_id=${levelId}`)
        .then(response => response.json())
        .then(data => {
          puzzleSelect.innerHTML = '<option value="">---------</option>';
          data.forEach(puzzle => {
            const option = document.createElement('option');
            option.value = puzzle.id;
            option.textContent = puzzle.name;
            puzzleSelect.appendChild(option);
          });
        });
    });
  }
});
