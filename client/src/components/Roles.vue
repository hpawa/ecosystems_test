<template>
  <div class="container-fluid">
    <navbar></navbar>
    <div class="row">
      <div class="col text-center">
        <h1>Roles</h1>
        <hr />
        <br />
        <br />
        <alert :message="message" v-if="showMessage"></alert>
        <button
          type="button"
          class="btn btn-success btn-sm"
          @click="initForm()"
          v-b-modal.role-modal
        >Add Role</button>
        <br />
        <br />
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(role, index) in roles" :key="index">
              <td>{{ role.name }}</td>
              <td>
                <button
                  type="button"
                  class="btn btn-warning btn-sm float-right"
                  @click="fillForm(role)"
                  v-b-modal.role-modal
                >Update</button>
                <button
                  type="button"
                  class="btn btn-danger btn-sm float-right"
                  @click="onDeleteRole(role)"
                >Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="roleModal" id="role-modal" :title="roleForm.title" hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-name-group" label="name:" label-for="form-name-input">
          <b-form-input
            id="form-name-input"
            type="text"
            v-model="roleForm.name"
            required
            placeholder="Enter name"
          ></b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from "axios";
import Alert from "./Alert.vue";
import NavBar from "./NavBar.vue";
export default {
  components: {
    alert: Alert,
    navbar: NavBar
  },
  data() {
    return {
      message: "",
      showMessage: false,
      roles: [],
      roleForm: {
        roleID: null,
        name: "",
        title: "",
        method: ""
      }
    };
  },
  methods: {
    getRoles() {
      const path = "http://localhost:5000/roles";
      axios
        .get(path)
        .then(res => {
          this.roles = res.data.roles;
        })
        .catch(error => {
          console.error(error);
        });
    },
    addRole(payload) {
      const path = "http://localhost:5000/roles";
      axios
        .post(path, payload)
        .then(res => {
          this.getRoles();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.getRoles();
        });
    },
    removeRole(roleID) {
      const path = `http://localhost:5000/roles/${roleID}`;
      axios
        .delete(path)
        .then(res => {
          this.getRoles();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.getRoles();
        });
    },
    updateRole(roleID, payload) {
      const path = `http://localhost:5000/roles/${roleID}`;
      axios
        .put(path, payload)
        .then(res => {
          this.getRoles();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.getRoles();
        });
    },
    onDeleteRole(role) {
      this.removeRole(role.id);
    },
    initForm() {
      this.roleForm.name = "";
      this.roleForm.title = "Add Role";
      this.roleForm.method = "POST";
    },
    fillForm(role) {
      this.roleForm.name = role.name;
      this.roleForm.title = "Update Role";
      this.roleForm.method = "PUT";
      this.roleForm.roleID = role.id;
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.roleModal.hide();
      const payload = {
        name: this.roleForm.name
      };
      if (this.roleForm.method == "POST") {
        this.addRole(payload);
      } else if (this.roleForm.method == "PUT") {
        this.updateRole(this.roleForm.roleID, payload);
      }
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.roleModal.hide();
      this.initForm();
    }
  },
  created() {
    this.getRoles();
  }
};
</script>