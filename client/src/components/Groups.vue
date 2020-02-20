<template>
  <div class="container-fluid">
    <navbar></navbar>
    <div class="row">
      <div class="col text-center">
        <h1>Groups</h1>
        <hr />
        <br />
        <br />
        <alert :message="message" v-if="showMessage"></alert>
        <button
          type="button"
          class="btn btn-success btn-sm"
          @click="initForm()"
          v-b-modal.group-modal
        >Add Group</button>
        <br />
        <br />
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Role</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(group, index) in groups" :key="index">
              <td>{{ group.name }}</td>
              <td>{{ group.role.name }}</td>
              <td>
                <b-button-group size="sm" class="float-right">
                  <b-button variant="warning" @click="fillForm(group)" v-b-modal.group-modal>Update</b-button>
                  <b-button variant="danger" @click="onDeleteGroup(group)">Delete</b-button>
                </b-button-group>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="groupModal" id="group-modal" :title="groupForm.title" hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-name-group" label="name:" label-for="form-name-input">
          <b-form-input
            id="form-name-input"
            type="text"
            v-model="groupForm.name"
            required
            placeholder="Enter name"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="form-role-group" label="Role:" label-for="form-role-select">
          <b-form-select
            id="form-role-select"
            v-model="groupForm.role"
            :options="rolesSelector"
            required
          ></b-form-select>
        </b-form-group>
        <b-button-group class="float-right">
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
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
      groups: [],
      roles: [],
      rolesSelector: [],
      groupForm: {
        groupID: null,
        name: "",
        role: null,
        title: "",
        method: ""
      }
    };
  },
  methods: {
    getGroups() {
      const path = "http://localhost:5000/groups";
      axios
        .get(path)
        .then(res => {
          this.groups = res.data.groups;
        })
        .catch(error => {
          console.error(error);
        });
    },
    getRoles() {
      const path = "http://localhost:5000/roles";
      axios
        .get(path)
        .then(res => {
          this.roles = res.data.roles;
          this.getRolesSelector();
        })
        .catch(error => {
          console.error(error);
        });
    },
    getRolesSelector() {
      this.rolesSelector.push({ value: null, text: "Select" });
      for (let i = 0; i < this.roles.length; i++) {
        let option = {};
        for (let key in this.roles[i]) {
          if (key == "id") {
            option["value"] = this.roles[i][key];
          } else if (key == "name") {
            option["text"] = this.roles[i][key];
          }
        }
        this.rolesSelector.push(option);
      }
    },
    addGroup(payload) {
      const path = "http://localhost:5000/groups";
      axios
        .post(path, payload)
        .then(res => {
          this.getGroups();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.getGroups();
        });
    },
    removeGroup(groupID) {
      const path = `http://localhost:5000/groups/${groupID}`;
      axios
        .delete(path)
        .then(res => {
          this.getGroups();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.getGroups();
        });
    },
    updateGroup(groupID, payload) {
      const path = `http://localhost:5000/groups/${groupID}`;
      axios
        .put(path, payload)
        .then(res => {
          this.getGroups();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch(error => {
          console.log(error);
          this.getGroups();
        });
    },
    onDeleteGroup(group) {
      this.removeGroup(group.id);
    },
    initForm() {
      this.groupForm.name = "";
      this.groupForm.role = null;
      this.groupForm.title = "Add Group";
      this.groupForm.method = "POST";
    },
    fillForm(group) {
      this.groupForm.name = group.name;
      this.groupForm.role = group.role.id;
      this.groupForm.title = "Update Group";
      this.groupForm.method = "PUT";
      this.groupForm.groupID = group.id;
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.groupModal.hide();
      const payload = {
        name: this.groupForm.name
      };
      if (this.groupForm.method == "POST") {
        this.addGroup(payload);
      } else if (this.groupForm.method == "PUT") {
        this.updateGroup(this.groupForm.groupID, payload);
      }
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.groupModal.hide();
      this.initForm();
    }
  },
  created() {
    this.getGroups();
    this.getRoles();
  }
};
</script>