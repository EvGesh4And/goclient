document.addEventListener('DOMContentLoaded', function() {
    const empTypeSelect = document.getElementById('emp_type');
    const departmentField = document.getElementById('department_field');
    const titleField = document.getElementById('title_field');
    
    if (empTypeSelect && departmentField && titleField) {
        empTypeSelect.addEventListener('change', function() {
            const type = this.value;
            
            departmentField.style.display = 'none';
            titleField.style.display = 'none';
            
            if (type === 'Manager') {
                departmentField.style.display = 'block';
            } else if (type === 'Director') {
                titleField.style.display = 'block';
            }
        });
        
        empTypeSelect.dispatchEvent(new Event('change'));
    }
});