// モーダルの開閉・フォーム操作用スクリプト
function openEditModal(student) {
    document.getElementById('modal-student-id').value = student.id;
    document.getElementById('modal-last-name').value = student.last_name;
    document.getElementById('modal-first-name').value = student.first_name;
    document.getElementById('modal-last-kana').value = student.last_kana;
    document.getElementById('modal-first-kana').value = student.first_kana;
    document.getElementById('modal-age').value = student.age;
    document.getElementById('edit-modal-backdrop').classList.add('active');
    document.getElementById('edit-modal').classList.add('active');
    var deleteBtn = document.getElementById('delete-btn');
    if (deleteBtn) {
        if (student.id) {
            deleteBtn.style.display = '';
        } else {
            deleteBtn.style.display = 'none';
        }
    }
}
function closeEditModal() {
    document.getElementById('edit-modal-backdrop').classList.remove('active');
    document.getElementById('edit-modal').classList.remove('active');
}
// イベントデリゲーションで削除ボタンのクリックを監視
document.addEventListener('click', function(e) {
    if (e.target && e.target.id === 'delete-btn') {
        if(confirm('本当に削除しますか？この操作は取り消せません。')) {
            var form = e.target.closest('form');
            if (form) form.submit();
        }
    }
}); 