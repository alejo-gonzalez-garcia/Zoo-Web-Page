function add_toast_to_body() {

}
$(document).ready(function() {

})
<div class="toast-container position-fixed top-0 start-50 translate-middle-x pt-3">
  <div id="liveToast" class="toast bg-danger" role="alert" aria-live="assertive" aria-atomic="true">
		<div class="d-flex">
			<div class="toast-body">
				<h4>aldf</h4>
				Hello, world! This is a toast message.
			</div>
			<button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
		</div>
  </div>
</div>
<script>
	const toastTrigger = document.getElementById('liveToastBtn')
	const toastLiveExample = document.getElementById('liveToast')
	if (toastTrigger) {
		toastTrigger.addEventListener('click', () => {
			const toast = new bootstrap.Toast(toastLiveExample)

			toast.show()
		})
	}
</script>
