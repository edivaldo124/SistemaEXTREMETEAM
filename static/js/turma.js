(() => {
    const campoData = document.getElementById('data-aula');
    campoData?.addEventListener('change', () => campoData.form?.requestSubmit());
})();
