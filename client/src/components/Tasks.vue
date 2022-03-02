<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Tasks</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.task-modal>Add Task</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Title</th>
              <th scope="col">Description</th>
              <th scope="col">Done?</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(task, id) in tasks" :key="id">
              <td>{{ task.title }}</td>
              <td>{{ task.description }}</td>
              <td>
                <span v-if="task.done">Yes</span>
                <span v-else>No</span>
              </td>
              <td>
                <button
                        type="button"
                        class="btn btn-warning btn-sm"
                        v-b-modal.task-update-modal
                        @click="editTask(task)">
                  Update
                </button>
                <button
                  type="button"
                  class="btn btn-danger btn-sm" @click="onDeleteTask(task)">
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addTaskModal"
             id="task-modal"
             title="Add a new task"
             hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-title-group"
                    label="Title:"
                    label-for="from-title-input">
        <b-form-input id="form-title-input"
                      type="text"
                      v-model="addTaskForm.title"
                      required
                      placeholder="Enter title">
        </b-form-input>
      </b-form-group>
      <b-form-group id="form-description-group"
                    label="Description:"
                    label-for="form-description-input">
        <b-form-input id="form-description-input"
                      type="text"
                      v-model="addTaskForm.description"
                      required
                      placeholder="Enter description">
        </b-form-input>
      </b-form-group>
      <b-form-group id="form-done-group">
        <b-form-checkbox-group id="form-checks">
          <b-form-checkbox value="true"
                           v-model="addTaskForm.done"
                           unchecked="false">
            Done?
          </b-form-checkbox>
        </b-form-checkbox-group>
      </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="editTaskModal"
             id="task-update-modal"
             title="Update"
             hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-title-edit-group"
                      label="Title:"
                      label-for="form-title-edit-input">
          <b-form-input id="form-title-edit-input"
                        type="text"
                        v-model="editTaskForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-description-edit-group"
                      label="Description:"
                      label-for="form-description-edit-input">
          <b-form-input id="form-description-edit-input"
                        type="text"
                        v-model="editTaskForm.description"
                        required
                        placeholder="Enter description">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-done-edit-group">
          <b-form-checkbox-group id="form-checks">
            <b-form-checkbox value="true"
                             unchecked="false"
                             v-model="editTaskForm.done">
              Done?
            </b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios'
import Alert from './Alert.vue'

export default {
  data () {
    return {
      tasks: [],
      addTaskForm: {
        title: '',
        description: '',
        done: []
      },
      message: '',
      showMessage: false,
      editTaskForm: {
        id: '',
        title: '',
        description: '',
        done: []
      }
    }
  },
  components: {
    alert: Alert
  },
  methods: {
    getTasks () {
      const path = 'http://localhost:5000/tasks'
      axios.get(path)
        .then((res) => {
          this.tasks = res.data.tasks
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        })
    },
    addTask (payload) {
      const path = 'http://localhost:5000/tasks'
      axios.post(path, payload)
        .then(() => {
          this.getTasks()
          this.message = 'Task added!'
          this.showMessage = true
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
          this.getTasks()
        })
    },
    initForm () {
      this.addTaskForm.title = ''
      this.addTaskForm.description = ''
      this.addTaskForm.done = []
      this.editTaskForm.id = ''
      this.editTaskForm.title = ''
      this.editTaskForm.description = ''
      this.editTaskForm.done = []
    },
    onSubmit (evt) {
      evt.preventDefault()
      this.$refs.addTaskModal.hide()
      let done = false
      if (this.addTaskForm.done) done = true
      const payload = {
        title: this.addTaskForm.title,
        description: this.addTaskForm.description,
        done // property shorthand
      }
      this.addTask(payload)
      this.initForm()
    },
    onReset (evt) {
      evt.preventDefault()
      this.$refs.addTaskModal.hide()
      this.initForm()
    },
    editTask (task) {
      this.editTaskForm = task
    },
    onSubmitUpdate (evt) {
      evt.preventDefault()
      this.$refs.editTaskModal.hide()
      let done = false
      if (this.editTaskForm.done) done = true
      const payload = {
        title: this.editTaskForm.title,
        description: this.editTaskForm.description,
        done // property shorthand
      }
      this.updateTask(payload, this.editTaskForm.id)
    },
    updateTask (payload, taskID) {
      const path = `http://localhost:5000/tasks/${taskID}`
      axios.put(path, payload)
        .then(() => {
          this.getTasks()
          this.message = 'Task updated!'
          this.showMessage = true
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.getTasks()
        })
    },
    onResetUpdate (evt) {
      evt.preventDefault()
      this.$refs.editTaskModal.hide()
      this.initForm()
      this.getTasks()
    },
    removeTask (taskID) {
      const path = `http://localhost:5000/tasks/${taskID}`
      axios.delete(path)
        .then(() => {
          this.getTasks()
          this.message = 'Task removed!'
          this.showMessage = true
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.getTasks()
        })
    },
    onDeleteTask (task) {
      this.removeTask(task.id)
    }
  },
  created () {
    this.getTasks()
  }
}
</script>
